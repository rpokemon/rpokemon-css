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
            if (len(lstrip) == 0 or lstrip.startswith('#') or lstrip.startswith('//')):
                continue
                
            line_data = line.split("=", 1)
            rep[("$" + line_data[0].strip() + "$")] = line_data[1].strip()

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
    get_vars()
    
    # Combine files in specified order
    with open('dist.css', 'wb') as outfile:
        with open('poketheme.css', 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)
                
    # Compress
    with open('dist.css', 'r+') as outfile:
        raw  = rep_vars(outfile.read()) # replace vars too
        mini = compress(raw)
        outfile.seek(0)
        outfile.write(top() + '\n' + mini)
        outfile.truncate()
        
        print('\nDone!')

if __name__ == '__main__':
    run()