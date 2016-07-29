import re
import os.path
import shutil
import glob
import time
import datetime
from csscompressor import compress

rep = {}

def get_vars():
    global rep
    with open("variables.dat", "r") as f:
        for line in f:
            lstrip = line.strip()
            
            # continue if empty line or commented line
            if (len(lstrip) == 0 or lstrip.startswith('#') or lstrip.startswith('//')):
                continue
            
            line_data = line.split("=", 1)
            
            # check valid variable name
            if (not line_data[0].strip().replace('_','').isalnum()):
                print('Error: Invalid variable name encountered; variables must be alphanumerical w/ optionally underscores')
                return False
                
            var_value = line_data[1].strip()
            
            # allow linking to another variable value that comes prior
            if (var_value.startswith('$') and var_value.endswith('$')):
                if (var_value in rep):
                    var_value = rep[var_value]
                else:
                    print('Error: variable as value not found ('+var_value+')')
                    return False
                
            rep[("$" + line_data[0].strip() + "$")] = var_value
    return True

def rep_vars(text):
    global rep
    
    if not rep:
        return text;
    
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text
            
def top():
    return (
        '/*CreatedBy:Hero_of_Legend,technophonix1,Atooz,kwwxis*/')

def run():
    global rep
    
    # load variables
    if (not get_vars()):
        return
    
    # Combine files in specified order
    with open('dist.css', 'wb') as outfile:
        with open('poketheme.css', 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)
                
    # Compress
    with open('dist.css', 'r+') as outfile:
        # read file and replace vars
        raw  = rep_vars(outfile.read())
        
        # check if any variables weren't replaced
        warning = ''
        var_sign = False
        var_name = ''
        vars_not_replaced = ''
        for ch in raw:
            if (not var_sign and ch == '$'): # starting "$"
                var_sign = True
            elif (var_sign):
                if (ch == '$'): # closing "$"
                    vars_not_replaced += '\n  - ' + var_name
                    var_name = ''
                elif (not ch.isalnum() and ch != '_'): # variables should be alphanumerical w/ underscores
                    var_sign = False
                    var_name = ''
                else:
                    var_name += ch
                    
        if (len(vars_not_replaced) > 0):
            warning = '\nWARNING: not all variables may have been properly replaced:' + vars_not_replaced
            print(warning)
            warning = '\n/*' + warning + '\n*/\n'
            
        # minify
        mini = compress(raw)
        outfile.seek(0)
        outfile.write(top() + '\n' + warning + mini)
        outfile.truncate()
        
        print('\nDone!')

if __name__ == '__main__':
    run()