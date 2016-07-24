
import os.path
import shutil
import glob
import time
import datetime
from csscompressor import compress

def top():
    return (
        '/*\n' +
        '    CSS theme for /r/pokemon \n' +
        '    Created by: Hero_of_Legend, technophonix1, Atooz, & kwwxis\n\n' +
        '    Unminified CSS is at https://github.com/matthew0x40/r-pokemon \n' +
        '        message /u/kwwxis with your github username for access\n\n' +
        '    >>> Please remember to commit and push once you\'re done with the stylesheet <<< \n'
        '*/'
        )

def run():
    # Combine files in specified order
    with open('dist.css', 'wb') as outfile:
        with open('poketheme.css', 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)
                
    # Compress
    with open('dist.css', 'r+') as outfile:
        raw  = outfile.read()
        mini = compress(raw)
        outfile.seek(0)
        outfile.write(top() + '\n' + mini)
        outfile.truncate()
        
        print('\nDone!')

if __name__ == '__main__':
    run()