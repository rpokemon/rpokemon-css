import unicodedata
import tinycss2

with open('dist.css', 'r+') as outfile:
    stylesheet_source  = outfile.read()
    
    nodes = tinycss2.parse_stylesheet(stylesheet_source)

    source_lines = stylesheet_source.splitlines()
    
    for line_number, line_text in enumerate(source_lines, start=1):
        for codepoint in line_text:
            # IE<8: *{color: expression\28 alert\28 1 \29 \29 }
            if codepoint == "\\":
                print('BACKSLASH')
                break
            # accept these characters that get classified as control
            elif codepoint in ("\t", "\n", "\r"):
                continue
            # Safari: *{font-family:'foobar\x03;background:url(evil);';}
            elif unicodedata.category(codepoint).startswith("C"):
                print('CONTROL_CHARACTER')
                break