
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