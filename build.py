#! python3
import os.path
import shutil
import glob
import time
import datetime
from csscompressor import compress

# -------------- FILE NAME ------------ PURPOSE --------------
               
order       = [ 'etc.css',            # body, buttons, and wiki
                'header.css',         # subreddit header
                'submit.css',         # submit form
                
                'linklisting.css',    # styles for the link listing page
                'thing.css',          # styles for thing elements (links and comments alike)
                'tagline.css',        # thing tagline
                'linkflair.css',      # link flair and filters
                
                'commentfix.css',     # styles for specifically comments
                'commentpage.css',    # styles for the comment page menus, usertext editor, etc.
                'usertextmd.css',     # styles for the markdown
                
                'sidecommon.css',     # sidebar common header and checkboxes
                'sidebar.css',        # sidebar
                'sidemd.css',         # sidebar md
                'sidecontentbox.css', # sidecontentbox
                
                'announce.css',       # announcements modules and bar
                
                'search.css',         # search page (does not include search input in sidebar, which is in sidebar.css)
                'footer.css',         # subreddit footer
                'modpages.css',       # any moderator pages that required additional CSS and also flair selector stuff
                
                'flair.css',          # user flairs
                'userflair.css',      # user flairs
                #'moontheme.css',      # night mode
                'banner.css',         # banner
                'sm_release.css',     # fancy CSS for Pokemon Sun & Moon Release Megathread
                'afd_suntheme.css', # Swap sun and moon themes
                'afd_moontheme.css', # Swap sun and moon themes
                'afd.css',            # april fools day 2017 source file
              ]      
                
# input/output variables
src_dir     = 'src'
dist_dir    = './'
dist_file   = 'dist.css'
unmin_file  = 'unmin.css'

def top(build_ver):
    return ('/*\n' +
            '  AFD CSS theme for /r/Pokemon; build #' + str(build_ver) + '\n' +
            '  Authors: Hero_of_Legend, technophonix1, Atooz, kwwxis & Haruka-sama' + '\n' +
            ' */')

def run():
    with open(r'build.dat','r+') as build:
        build_ver = int(build.read()) + 1
        print('\nBUILD #' + str(build_ver))
        
        if not os.path.isdir(src_dir):
            print('\nFailed: the source directory, "' + src_dir + '" was not found')
            return
            
        # Combine files in specified order
        with open(dist_dir + '\\' + dist_file, 'wb') as outfile:
            for src_file in order:
                path = src_dir + '\\' + src_file
                
                if os.path.isfile(path):
                    with open(path, 'rb') as readfile:
                        shutil.copyfileobj(readfile, outfile)
                        print('  + ' + path)
                else:
                    print('\nFailed: target file not found: ' + path + ';\n' +
                    'if this file is no longer in use then you must remove it from the "order" variable in build.py')
                    return
        
        # copy an unminified version of the stylesheet to a separate file
        shutil.copyfile(dist_dir + '\\' + dist_file, dist_dir + '\\' + unmin_file);
        
        # Compress
        with open(dist_dir + '\\' + dist_file, 'r+') as outfile:
            raw  = outfile.read()
            mini = compress(raw)
            outfile.seek(0)
            outfile.write(top(build_ver) + '\n' + mini)
            outfile.truncate()
            
        # Increment build version in build.dat afterwards in case of failure
        build.seek(0)
        build.write(str(build_ver))
        
        print('\nDone!')

if __name__ == '__main__':
    run()
