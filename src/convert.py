#!/usr/bin/python
import fontforge
import sys

def main(argv):
    print '-------------------------------------'
    print '|          Font Converter            |'
    print '-------------------------------------'
    print ''
    fullpath = argv[0].decode("GBK")
    targetpath = argv[1].decode("GBK")
    font = fontforge.open(fullpath)
    font.generate(targetpath)
    print 'Convert done!'
    print ''
    print '-------------------------------------'
    print '|          Font Converter            |'
    print '-------------------------------------'
    print '| Version: 1.0.0 2015.11.8           |'
    print '-------------------------------------'
    print ''

if __name__ == '__main__':
    main(sys.argv[1:])