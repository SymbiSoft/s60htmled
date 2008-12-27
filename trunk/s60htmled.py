# s60htmled.py: Simple HTML editor for S60 Ed.3 smartphones
# 
# Copyright (C) Dmitri Brechalov, 2008
#
# Project URL: http://code.google.com/p/s60htmled/
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

import appuifw2
import e32
import key_codes
import os, sys
#### in case the program runs as a script
sys.path.append('C:\\Python')
sys.path.append('E:\\Python')

from utils import *
from xtext import xText

UID = u"e3e34da2"
VERSION = '0.7.1'

htmltemplates = (
    '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<title></title>
</head>
<body>

</body>
</html>
''',
'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<title></title>
</head>
<body>

</body>
</html>
'''
)

class HTMLEditor(xText):
    '''HTML Editor. Uses appuifw2.Text
    '''
    version = VERSION
    title = u('HTML Editor %s' % (version))
#     def __init__(self):
#         xText.__init__(self)

    #### Help
    
    def aboutDlg(self):
        appuifw2.query(u('S60 HTML Editor\nVersion %s\n(C) Dmitri Brechalov, 2008' % (self.version)), 'query', ok=u(''), cancel=u('Close'))

    def showUID(self):
        appuifw2.query(appuifw2.app.uid(), 'query')
        
    def helpDlg(self):
        topics = (u('Call button works as functional key.\nCall + arrows: Page Up, Page Down, Line Start and Line End.'),
                  u('Press Call + Select to go to the top/bottom of the text or goto line.'),
                  u('Press right softkey to select and insert HTML tag.\nSelect "Custom tag" to insert any tag.'),
                  u('Press Call + Right softkey to insert HTML entity.'),
                  u('More info and fresh version are available at http://code.google.com/p/s60htmled/'),
                 )
        for t in topics:
            if not appuifw2.query(t, 'query', ok=u('Next'), cancel=u('Close')):
                break

    #### Extra file operations

    def fileTemplate(self):
        if self.notSaved():
            if not self.fileSave(): return
        ans = appuifw2.popup_menu([u('Simple HTML'), u('HTML 4.01 Transitional')], u('Select template'))
        if ans is None: return
        self.fileNew()
        self.editor.set(u(htmltemplates[ans]))
        self.editor.set_pos(0)
        self.editor.has_changed = False
        
    def launchBrowser(self):
        if not self.fname or self.notSaved():
            if not self.fileSave(): return
        appuifw2.Content_handler().open(u(self.fname.replace('/', '\\')))

    #### Working with tags

    def attrjoin(self, attrs):
        return ' ' + ' '.join([ '%s="%s"' % (k, v) for k, v in attrs.items() ])
        
    def addTag(self, tag, attrs=None, needCloseTag=True):
        (pos, anchor, text) = self.editor.get_selection()
        if attrs:
            sattr = self.attrjoin(attrs)
        else:
            sattr = ''
        if needCloseTag:
            text = '<%s%s>%s</%s>' % (tag, sattr, s(text), tag)
        else:
            text = '<%s%s/>' % (tag, sattr)
        if pos > anchor:
            pos, anchor = anchor, pos
        self.editor.delete(pos, anchor-pos)
        self.editor.set_pos(pos)
        self.editor.add(u(text))

    def askAttr(self, tag):
        result = dict()
        while True:
            ans = appuifw2.query(u("<%s%s...>\nAttribute:" % (tag, self.attrjoin(result))), 'text', )
            if ans is None: break
            result[s(ans).lower()] = ""
        if len(result.keys()) == 0:
            return None
        return result
    
    def insertTag(self):
        ####    tag           (askForAttr, needCloseTag)
        tags = {'a':          (True, True),
                'img':        (True, False),
                'h1':         (False, True),
                'h2':         (False, True),
                'h3':         (False, True),
                'h4':         (False, True),
                'h5':         (False, True),
                'h6':         (False, True),
                'strong':     (False, True),
                'em':         (False, True),
                'code':       (False, True),
                'pre':        (False, True),
                'u':          (False, True),
                'b':          (False, True),
                'i':          (False, True),
                'p':          (True, True),
                'ul':         (False, True),
                'ol':         (False, True),
                'li':         (False, True),
                's':          (False, True),
                'q':          (False, True),
                'blockquote': (False, True),
                'var':        (False, True),
                'tt':         (False, True),
                'br':         (False, False),
                'hr':         (False, False),
                }
        tlst = tags.keys()
        tlst.sort()
        ans = appuifw2.selection_list(map(u, ['Custom...'] + tlst), 1)
        if ans is None: return
        if ans == 0:
            self.insertCustomTag()
        else:
            tag = tlst[ans-1]
            (askForAttr, needCloseTag) = tags[tag]
            if askForAttr:
                attr = self.askAttr(tag)
            else:
                attr = None
            self.addTag(tag, attr, needCloseTag)

    def insertCustomTag(self):
        ans = appuifw2.query(u('HTML Tag:'), 'text')
        if not ans: return
        tag = s(ans).lower()
        attr = self.askAttr(tag)
        self.addTag(tag, attr, True)

    def insertEntity(self):
        ans = appuifw2.popup_menu(map(u, ('&', '<', '>', '"')))
        if ans is None: return
        self.addEntity(('amp', 'lt', 'gt', 'quot')[ans])

    def addEntity(self, ent):
        self.editor.add(u('&%s;' % ent))

    def quit(self):
        if self.notSaved():
            if not self.fileSave(): return
        self.app_lock.signal()
        if appuifw2.app.uid() == UID:
            appuifw2.app.set_exit() # running as app

    def run(self):
        self.app_lock = e32.Ao_lock()
        appuifw2.app.menu = [
            (u("File"), ((u("Open"), self.fileOpen),
                         (u("Save"), self.fileSave),
                         (u("Save as"), self.fileSaveAs),
                         (u("New"), self.fileNew),
                         (u("New from template"), self.fileTemplate),
                         (u("View in browser"), self.launchBrowser),)),
            (u("Edit"), ((u("Undo"), self.undo),
                         (u("Cut"), self.cut),
                         (u("Copy"), self.copy),
                         (u("Paste"), self.paste),
                         (u("Select All"), self.selectAll),
                         (u("Select None"), self.selectNone))),
            (u("Search"), ((u("Find Forward"), self.findTextForward),
                           (u("Find Backward"), self.findTextBackward),
                           (u("Replace"), self.replaceText))),
            (u("Help"), ((u("Help"), self.helpDlg),
                         (u("About"), self.aboutDlg),)),
            (u("Exit"), self.quit)
            ]
        self.bindExitKey((u('Tag'), self.insertTag), (u('Entity'), self.insertEntity))
        self.editor.has_changed = False
        self.fileNew()
        e32.ao_yield()
        appuifw2.app.body = self.editor

        old_exit_key_text = appuifw2.app.exit_key_text
        old_menu_key_text = appuifw2.app.menu_key_text
        appuifw2.app.menu_key_text = u("Options")
        self.rebindFunKeys()
        self.app_lock.wait()
        appuifw2.app.exit_key_text = old_exit_key_text

if __name__ == '__main__':
    editor = HTMLEditor()
    editor.run()
