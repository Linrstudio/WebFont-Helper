#!/usr/bin/python

# Copyright 2010, Google Inc.
# Author: Raph Levien (<firstname.lastname>@gmail.com)
# Author: Dave Crossland (dave@understandinglimited.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# A script for subsetting a font, using FontForge. See README for details.
#
# Modified by xiaogezi. 2015.11
# Author: xiaogezi(<www@xiaogezi.cn>)

import fontforge
import sys
import getopt
import os
import ctypes
import string
import re

def select_with_refs(font, unicode, newfont, pe = None, nam = None):
    newfont.selection.select(('more', 'unicode'), unicode)
    if nam:
        print >> nam, "0x%0.4X" % unicode, fontforge.nameFromUnicode(unicode)
    if pe:
        print >> pe, "SelectMore(%d)" % unicode
    try:
        for ref in font[unicode].references:
            #print unicode, ref
            newfont.selection.select(('more',), ref[0])
            if nam:
                print >> nam, "0x%0.4X" % ref[0], fontforge.nameFromUnicode(ref[0])
            if pe:
                print >> pe, 'SelectMore("%s")' % ref[0]
    except:
        print 'Resolving references on u+%04x failed' % unicode

def subset_font_raw(font_in, font_out, unicodes, opts):
    if '--namelist' in opts:
        # 2010-12-06 DC To allow setting namelist filenames, 
        # change getopt.gnu_getopt from namelist to namelist= 
        # and invert comments on following 2 lines
        # nam_fn = opts['--namelist']
        nam_fn = font_out + '.nam'
        nam = file(nam_fn, 'w')
    else:
        nam = None
    if '--script' in opts:
        pe_fn = "/tmp/script.pe"
        pe = file(pe_fn, 'w')
    else:
        pe = None
    font = fontforge.open(font_in)
    if pe:
      print >> pe, 'Open("' + font_in + '")'
      # Note: should probably do this in the non-script case too
      # see http://sourceforge.net/mailarchive/forum.php?thread_name=20100906085718.GB1907%40khaled-laptop&forum_name=fontforge-users
      # but FontForge's python API can't toggle winasc/desc as offset, only set the offset values with font.os2_windescent and font.os2_winascent
      print >> pe, 'SetOS2Value("WinAscentIsOffset", 0)'
      print >> pe, 'SetOS2Value("WinDescentIsOffset", 0)'
    for i in unicodes:
        select_with_refs(font, i, font, pe, nam)

    addl_glyphs = []
    if '--nmr' in opts: addl_glyphs.append('nonmarkingreturn')
    if '--null' in opts: addl_glyphs.append('.null')
    for glyph in addl_glyphs:
        font.selection.select(('more',), glyph)
        if nam:
            print >> nam, "0x%0.4X" % fontforge.unicodeFromName(glyph), glyph
        if pe:
            print >> pe, 'SelectMore("%s")' % glyph

    flags = ()

    if '--simplify' in opts:
        font.simplify()
        font.round()
        flags = ('omit-instructions',)

    if '--strip_names' in opts:
        font.sfnt_names = ()

    if '--new' in opts:
        font.copy()
        new = fontforge.font()
        new.encoding = font.encoding
        new.em = font.em
        new.layers['Fore'].is_quadratic = font.layers['Fore'].is_quadratic
        for i in unicodes:
            select_with_refs(font, i, new, pe, nam)
        new.paste()
        # This is a hack - it should have been taken care of above.
        font.selection.select('space')
        font.copy()
        new.selection.select('space')
        new.paste()
        new.sfnt_names = font.sfnt_names
        font = new
    else:
        font.selection.invert()
        print >> pe, "SelectInvert()"
        font.cut()
        print >> pe, "Clear()"

    if nam: 
        print "Writing NameList", 
        nam.close()
        print nam

    if pe:
        print >> pe, 'Generate("' + font_out + '")'
        pe.close()
        os.system("fontforge -script " + pe_fn)
    else:
        font.generate(font_out, flags = flags)
        print '\tDone'
    font.close()

    if '--roundtrip' in opts:
        font2 = fontforge.open(font_out)
        font2.generate(font_out, flags = flags)

    print '-------------------------------------'
    print '|           WebFont Subset           |'
    print '-------------------------------------'
    print '| Version: V1.0  2015.11            |'
    print '-------------------------------------'

def subset_font(font_in, font_out, unicodes, opts):
    font_out_raw = font_out
    if not font_out_raw.endswith('.ttf'):
        font_out_raw += '.ttf';
    subset_font_raw(font_in, font_out_raw, unicodes, opts)
    if font_out != font_out_raw:
        os.rename(font_out_raw, font_out)
        os.rename(font_out_raw + '.nam', font_out + '.nam')

def getsubset(subset):
    subsets = subset.split('+')

    quotes  = [0x2013] # endash
    quotes += [0x2014] # emdash
    quotes += [0x2018] # quoteleft
    quotes += [0x2019] # quoteright
    quotes += [0x201A] # quotesinglbase
    quotes += [0x201C] # quotedblleft
    quotes += [0x201D] # quotedblright
    quotes += [0x201E] # quotedblbase
    quotes += [0x2022] # bullet
    quotes += [0x2039] # guilsinglleft
    quotes += [0x203A] # guilsinglright

    latin  = range(0x20, 0x7f) # Basic Latin (A-Z, a-z, numbers)
    latin += range(0xa0, 0x100) # Western European symbols and diacritics
    latin += [0x20ac] # Euro
    latin += [0x0152] # OE
    latin += [0x0153] # oe
    latin += [0x003b] # semicolon
    latin += [0x00b7] # periodcentered
    latin += [0x0131] # dotlessi
    latin += [0x02c6] # circumflex
    latin += [0x02da] # ring
    latin += [0x02dc] # tilde
    latin += [0x2074] # foursuperior
    latin += [0x2215] # divison slash
    latin += [0x2044] # fraction slash
    latin += [0xe0ff] # PUA: Font logo
    latin += [0xeffd] # PUA: Font version number
    latin += [0xf000] # PUA: font ppem size indicator: run `ftview -f 1255 10 Ubuntu-Regular.ttf` to see it in action!

    result = quotes 
    if 'latin' in subset:
        result += latin
    if 'latin-ext' in subset:
        # These ranges include Extended A, B, C, D, and Additional with the
        # exception of Vietnamese, which is a separate range
        result += (range(0x100, 0x250) +
                   range(0x1e00, 0x1ea0) +
                   range(0x1ef2, 0x1f00) +
                   range(0x20a0, 0x20d0) +
                   range(0x2c60, 0x2c80) +
                   range(0xa720, 0xa800))
    if 'vietnamese' in subset:
        result += range(0x1ea0, 0x1ef2) + [0x20ab]
    if 'greek' in subset:
        # Could probably be more aggressive here and exclude archaic characters,
        # but lack data
        result += range(0x370, 0x400)
    if 'greek-ext' in subset:
        result += range(0x370, 0x400) + range(0x1f00, 0x2000)
    if 'cyrillic' in subset:
        # Based on character frequency analysis
        result += range(0x400, 0x460) + [0x490, 0x491, 0x4b0, 0x4b1]
    if 'cyrillic-ext' in subset:
        result += (range(0x400, 0x530) +
                   [0x20b4] +
                   range(0x2de0, 0x2e00) +
                   range(0xa640, 0xa6a0))
    return result

def main(argv):
    print '-------------------------------------'
    print '|          WebFont Subset            |'
    print '-------------------------------------'
    print ''
    print '1. args'
    optlist, args = getopt.gnu_getopt(argv, '', ['clipboard', 'no_latin', 'new_name=', 'string=', 'strip_names',
                                                 'simplify', 'new', 'script',
                                                 'nmr', 'roundtrip', 'subset=', 
                                                 'namelist', 'null'])

    font_in, font_out = args
    opts = dict(optlist)
    if '--string' in opts:
        strin = opts['--string'].decode("GBK")
        subset = map(ord, strin)
        print '\t--string: [' + strin + ']'
    else:
        if '--clipboard' in opts:
            CF_TEXT = 1
			
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            user32.OpenClipboard(0)
            if user32.IsClipboardFormatAvailable(CF_TEXT):
            	data = user32.GetClipboardData(CF_TEXT)
            	data_locked = kernel32.GlobalLock(data)
            	text = ctypes.c_char_p(data_locked)
                clipboard_txt = text.value.decode("GBK")
            	print('\t--clipboard: [\n' + clipboard_txt + '\n]')
            	if '--no_latin' in opts:
            		subset = map(ord, re.sub('[a-zA-Z0-9~`!@#$%^&*()-_=+;:\'\",<>?\{\}\[\]\/\\. \t\n\r\f\v]+','' , clipboard_txt))
            	else:
            		subset = map(ord, clipboard_txt)
            	kernel32.GlobalUnlock(data_locked)
            else:
            	print('\tNo Clipboard Content')

            user32.CloseClipboard()
        else:
			subset = getsubset(opts.get('--subset', 'latin'))
    new_name = 'webfont'	
    if '--new_name' in opts:
        new_name = opts['--new_name'].decode("GBK")
        print '\t--new_name: ' + new_name
    print ''
    print '2. Set output path'
    print '\t' + font_out + '\\' + new_name + '.ttf'
    print ''
    print '3. Subset'
    subset_font(font_in, font_out + '\\' + new_name + '.ttf', subset, opts)
if __name__ == '__main__':
    main(sys.argv[1:])

