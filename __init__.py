# -*- coding: utf-8 -*-
import sys
print('init run...')
#sys.path.append(__name__ + '/uidesign')
print(__name__)
#__import__(__package__ + '.uidesign')
#import()
import os, glob, subprocess
def makeUiFiles():
    p = os.path.realpath('.')
    for f in glob.glob(p + '/uidesign/*.ui'):
        print(subprocess.run('pyuic5 ' + f + ' -o ' + f.replace('.ui', '.py'), shell=True))
#print(pathlib.Path('.'))
#print(os.path.realpath('.'))
makeUiFiles()