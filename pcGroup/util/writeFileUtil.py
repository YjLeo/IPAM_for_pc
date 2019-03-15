#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib

def writeFile(filePath , content , unquote = False):
    try:
        contentLast = content
        if unquote == True:
            contentLast = urllib.unquote(content)
        with open(filePath,'w') as f:
            f.write(contentLast.replace('\n',"\n<br/>\n"))
            f.closed
        return True
    except:
        return False