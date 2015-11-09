# Created by xiaogezi. 2015.11
# Author: xiaogezi(<www@xiaogezi.cn>)

import fontforge;
import os
import sys
import locale
print locale.getdefaultlocale()
reload(sys)
sys.setdefaultencoding('gbk')
import psMat
import string
import subprocess
import time
import getopt

def ttf2eot(ttfpath, ttffolder, fn, srcFolder, srcFn):
    scriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    time.sleep(1)
    print ''
    print '4. Convert ttf to eot'
    print '\t[Run]"' + scriptPath + '\\ttf2eot.exe"' + ' "' + ttfpath + '" "' + ttffolder + '.eot"'
    print ''
    print ("\t[cmd] copy '%s' '%s'" % (ttffolder + '.ttf', os.path.expanduser('~') + "\\" + fn))
    print ''
    hmoePath = os.path.expanduser('~') + "\\" + fn + '.ttf'
    os.system ('copy "%s" "%s"' % (ttffolder + '.ttf', hmoePath))
    subprocess.Popen('"' + scriptPath + '\\ttf2eot.exe"' + ' "' + hmoePath + '" "' + ttffolder + '.eot"')
    print ''
    print "\tConvert ttf to eot done"
    print "5. Rename filename"
    srcFile = srcFolder + '\\' + srcFn
    print '\tsource file: ' + srcFile
    srcFileName = os.path.dirname(srcFile)
    targetFolder = os.path.dirname(ttffolder)
    targetFilename = os.path.basename(srcFile).split('.')[0]
    targetPath = targetFolder + '\\' + fn
    print ('\t[cmd] move "%s" "%s"' % (srcFile, targetPath + '.src.ttf'))
    os.system ('move "%s" "%s"' % (srcFile, targetPath + '.src.ttf'))
    print ('\t[cmd] move "%s" "%s"' % (ttffolder + '.eot', targetPath + '.eot'))
    os.system ('move "%s" "%s"' % (ttffolder + '.eot', targetPath + '.eot'))
    print ('\t[cmd] move "%s" "%s"' % (ttffolder + '.woff', targetPath + '.woff'))
    os.system ('move "%s" "%s"' % (ttffolder + '.woff', targetPath + '.woff'))
    print ('\t[cmd] move "%s" "%s"' % (ttffolder + '.svg', targetPath + '.svg'))
    os.system ('move "%s" "%s"' % (ttffolder + '.svg', targetPath + '.svg'))
    print ('\t[cmd] move "%s" "%s"' % (ttffolder + '.ttf', targetPath + '.ttf'))
    os.system ('move "%s" "%s"' % (ttffolder + '.ttf', targetPath + '.ttf'))
    print '\t Rename filename done'
    print ''
    print '-------------------------------------'
    print '|     Font Converter (Transform)     |'
    print '-------------------------------------'
    print '| Version: V1.0  2015.11            |'
    print '-------------------------------------'
    return

def main(argv):
    optlist, args = getopt.gnu_getopt(argv, '', ['scaleX=', 'scaleY=', 'new_name='])
    print '-------------------------------------'
    print '|     Font Converter (Transform)     |'
    print '-------------------------------------'
    print ''
    print '1. args'
    opts = dict(optlist)
    flags = ()
    flags += ('opentype',)
    fullpath = argv[0].decode("GBK")
    fileName = os.path.basename(fullpath)
    newFileName = fileName.split('.')[0] + '.ok'
    argScaleX = '1'
    argScaleY = '1'
    if '--new_name' in opts:
        newFileName = opts['--new_name'].decode("GBK")
        print '\t--new_name: ' + newFileName
    if '--scaleX' in opts:
        argScaleX = opts['--scaleX'].decode('utf-8')
        print '\t--scaleX: ' + argScaleX
    if '--scaleY' in opts:
        argScaleY = opts['--scaleY'].decode('utf-8')
        print '\t--scaleY: ' + argScaleY
    font = fontforge.open(fullpath)
    font.selection.all()
    if argScaleX != '':
        print '\tTransform font'
        font.transform(psMat.scale(float(argScaleX), float(argScaleY)))
        print '\ttransform: (' + str(float(argScaleX)) + ', ' + str(float(argScaleY)) + ')'
        print ''
    folder = os.path.dirname(fullpath)
    font.copyright = 'Modified By xiaogezi'
    print ''
    print '2. Convert ttf to woff, svg'
    font.generate(folder + '\\' + newFileName + '.ttf')
    font.generate(folder + '\\' + newFileName + '.woff', flags = flags)
    font.generate(folder + '\\' + newFileName + '.svg')
    glyphArr = []
    for glyph in font:
        glyphArr.append(font[glyph].unicode)
        #glyphname#encoding
    font.close()
    print '\tGlyphs: '
    print glyphArr
    print "\tConvert done"
    print ''
    print "3. Generator HTML DEMO"
    srcFileName = newFileName
    fs = open(folder + '\\' + newFileName + '.hta', 'w')
    fs.write('<!DOCTYPE html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1" /><meta http-equiv="X-UA-Compatible" content="IE=edge" /><style>@font-face{font-family:\'xiaogezi\';src:url(\'' + srcFileName + '.eot\');src:url(\'' + srcFileName + '.eot?#iefix\') format(\'embedded-opentype\'),url(\'' + srcFileName + '.woff\') format(\'woff\'),url(\'' + srcFileName + '.ttf\') format(\'truetype\'),url(\'' + srcFileName + '.svg#webfont\') format(\'svg\');}body{padding:50px;font:300 25px/2 \'xiaogezi\' normal;}html{color:#000;background:#FFF;}input[type=button]{padding:8px 10px;overflow:visible;vertical-align:middle;min-width:60px;-webkit-appearance:none;}.bg{background:#000;color:#FFF;}</style></head><body><div class="ui-cmd" id="js_cmd"><input type="button" value="Bold" data-cmd="bold" /> <input type="button" value="-" data-cmd="-1"/> <input type="button" value="+" data-cmd="1" /> <input type="button" value="BgColor" data-cmd="bg" /> <span class="size-text"></span></div><div class=""><div class="str" id="webfontshow" contenteditable="true"><script>var arr = ' + str(glyphArr) + ';for(var i = 0, j = arr.length, cur;i < j; ++ i){cur = arr[i];cur != -1 && document.write(\'<span onclick="clipboardData.setData(\\\'text\\\', \\\'&amp;#\' + cur + \';\\\');" data-html="&amp;#\' + cur + \';" data-css="\\\\\' + cur + \'" data-string="\' + String.fromCharCode(cur) + \'">&#\' + cur + \';</span>\');};</script></div></div><script src="http://libs.baidu.com/jquery/1.11.1/jquery.min.js"></script><script>(function($){function hashChanged(){$(\'html\').toggleClass(\'bg\', location.hash == \'#bg\');};$(\'#js_cmd\').delegate(\'input:button\', \'click\', function(e){var me = $(this), cmd = me.data(\'cmd\'), ctrlKey = e.ctrlKey;if(cmd == \'bold\'){var weight = $(\'.str\').css(\'fontWeight\');$(\'.str\').css(\'font-weight\', weight == 400 ? \'bold\' : 400);}else if(cmd == \'bg\'){location.href = location.hash.indexOf(\'bg\') > -1 ? \'#\' : \'#bg\';hashChanged();}else{ctrlKey && (cmd = cmd * 5);var size = $(\'.str\').css(\'fontSize\'),val = parseInt(size, 10) + cmd;$(\'.str\').css(\'fontSize\', val);$(\'.size-text\').text(val + \'px\');}});$(window).bind(\'hashchange\', hashChanged);})(jQuery);</script></body></html>')
    fs.flush()
    fs.close()
    print  '\tttf2eot(' + folder + '\\' + newFileName + '.ttf' + ',' + folder + '\\' + newFileName + ',' + newFileName + ',' + folder + ',' + fileName + ')'
    ttf2eot(folder + '\\' + newFileName + '.ttf', folder + '\\' + newFileName, newFileName, folder, fileName)
    return

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1:])
    else:
        print "Usage: <input font> <output font name> <--scaleX=.85>"
        print " Specify output font without file extension."