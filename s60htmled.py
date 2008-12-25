# s60htmled.py: Simple HTML editor for S60 Ed.3 smartphones
# 
# Copyright (C) Dmitri Brechalov, 2008
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
import os

VERSION = '0.6.a'

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

u = lambda s: s.decode('utf-8')
s = lambda s: s.encode('utf-8')

schedule = appuifw2.schedule

def fileBrowser(label, dironly=False, dirname=''):
    isdir = lambda fname: os.path.isdir(os.path.join(dirname, fname))
    isfile = lambda fname: not os.path.isdir(os.path.join(dirname, fname))
    markdir = lambda fname: fname + '/'
    def chkdir(d):      # os.path uses '/' as a dir separator but os.path.join
        d = s(d)        # adds no '/' between drive name and file path
        if not (d.endswith('/') or d.endswith('\\')):
            return d + '/'      # content handler return an error when there is
        else:                   # no separator after drive name
            return d
    while True:
        if not dirname:
            items = map(chkdir, e32.drive_list())
        else:
            lst = os.listdir(dirname)
            dirs = map(markdir, filter(isdir, lst))
            dirs.sort()
            if not dironly:
                files = filter(isfile, lst)
                files.sort()
            else:
                files = []
            items = ['..'] + dirs + files
        ans = appuifw2.popup_menu(map(u, items), u(label))
        if ans is None: return None
        fname = items[ans]
        if fname == '..':
            return fname
        fname = os.path.join(dirname, fname)
        if os.path.isdir(fname):
            ans = fileBrowser(fname, dironly, fname)
            if ans != '..': return ans
            if dironly and ans == '..': return fname
        else:
            return fname

class xText(object):
    '''eXtended Text editor
    '''
    def __init__(self):
        self.editor = appuifw2.Text(move_callback=self.moveEvent, edit_callback=self.changeEvent, skinned=True)
        self.editor.style = appuifw2.STYLE_BOLD
#         self.editor.color = (0, 0, 0)
        self.fname = None
        self.tags = []
        self.hdr = None
        self.find_text = u('')
        self.replace_text = u('')
        self.old_indicator = self.editor.indicator_text
        self.funkey_timer = None

    def dummy(self):
        appuifw2.note(u('Not implmented yet!'), 'error')
    
    def notSaved(self):
        if self.editor.has_changed:
            return appuifw2.query(u('File has been changed. Save?'), 'query', ok=u('Yes'), cancel=u('No'))
        return False

    def changeEvent(self, pos, num):
        self.updateIndicator()

    def moveEvent(self):
        schedule(self.updateIndicator)

    def updateIndicator(self):
        try:
            text_pos = self.editor.get_pos()
            text_len = self.editor.len()
            pos = int(round(float(text_pos) / float(text_len) * 100))
        except ZeroDivisionError:
            pos = 0
        self.editor.indicator_text = u('%s%%' % pos)

    def yesKeyPressed(self):
        self.bindFunKeys()

    def bindFunKeys(self):
        in_time = (self.funkey_timer is not None)
        if in_time:
            self.funkey_timer.cancel()
        self.funkey_timer = e32.Ao_timer()
        self.funkey_timer.after(1.5, self.rebindFunKeys)
        pos = self.editor.get_pos()
        self.editor.bind(key_codes.EKeyUpArrow,    lambda : self.arrowKeyPressed(pos, appuifw2.EFPageUp))
        self.editor.bind(key_codes.EKeyDownArrow,  lambda : self.arrowKeyPressed(pos, appuifw2.EFPageDown))
        self.editor.bind(key_codes.EKeyLeftArrow,  lambda : self.arrowKeyPressed(pos, appuifw2.EFLineBeg))
        self.editor.bind(key_codes.EKeyRightArrow, lambda : self.arrowKeyPressed(pos, appuifw2.EFLineEnd))
        self.editor.bind(key_codes.EKeySelect,     self.moveMenu)
        self.editor.bind(key_codes.EKeyYes,        self.rebindFunKeys)
        self.old_indicator = self.editor.indicator_text
        appuifw2.app.exit_key_handler = self.rightSoftkeyPressed
        appuifw2.app.exit_key_text = u("Entity")
        self.editor.indicator_text = u('Func')
        
    def rebindFunKeys(self):
        in_time = (self.funkey_timer is not None)
        if in_time:
            self.funkey_timer.cancel()
            self.funkey_timer = None
        for key in (key_codes.EKeyUpArrow, key_codes.EKeyDownArrow, key_codes.EKeyLeftArrow, key_codes.EKeyRightArrow, key_codes.EKeySelect):
            self.editor.bind(key, lambda : None)
        self.editor.bind(key_codes.EKeyYes, self.yesKeyPressed)
        self.editor.bind(key_codes.EKeyStar, self.starKeyPressed)
        self.editor.indicator_text = self.old_indicator
        appuifw2.app.exit_key_handler = self.insertTag
        appuifw2.app.exit_key_text = u("Tag")

    def starKeyPressed(self):
        appuifw2.note(u('Star key pressed'))
        e32.ao_yeld()

    def arrowKeyPressed(self, pos, cmd):
        self.rebindFunKeys()
        schedule(self.moveCursor, pos, cmd)

    def rightSoftkeyPressed(self):
        self.rebindFunKeys()
        schedule(self.insertEntity)

    def moveCursor(self, pos, cmd):
        self.editor.set_pos(pos)
        self.editor.move(cmd)
        self.moveEvent()

    def moveToLine(self, line):
        self.editor.focus = False
        self.editor.set_pos(0)
        for i in range(line-1):
            self.editor.move(appuifw2.EFLineDown)
        self.editor.focus = True
        self.moveEvent()

    def gotoLine(self):
        ans = appuifw2.query(u("Goto line"), 'number', 1)
        if ans:
            schedule(self.moveToLine, ans)

    def moveMenu(self):
        self.rebindFunKeys()
        ans = appuifw2.popup_menu([u('Top'), u('Bottom'), u('Goto line')])
        if ans is not None:
            if ans == 0:
                schedule(self.moveCursor, 0, appuifw2.EFNoMovement)
            elif ans == 1:
                schedule(self.moveCursor, len(self.editor.get()), appuifw2.EFNoMovement)
            elif ans == 2:
                schedule(self.gotoLine)
        self.moveEvent()

    def doFind(self, find_text, fwd=True):
        if fwd:
            txt = self.editor.get()[self.editor.get_pos():]
            i = txt.find(find_text)
        else:
            txt = self.editor.get()[:self.editor.get_pos()-1]
            i = txt.rfind(find_text)
        if i >= 0:
            if fwd:
                pos = self.editor.get_pos() + i + len(find_text)
            else:
                pos = i + len(find_text)
            self.editor.set_pos(pos)
            self.moveEvent()
            return True
        appuifw2.note(u("Not found"), "info")
        return False
    
    def doReplace(self, txt):
        ed = self.editor
        pos = ed.get_pos()-len(self.find_text)
        ed.delete(pos, len(self.find_text))
        ed.set_pos(pos)
        ed.add(txt)
        ed.set_pos(pos + len(txt))
    
    def findTextForward(self):
        ans = appuifw2.query(u("Find forward"), "text", self.find_text)
        if ans is None: return
        self.find_text = ans
        if self.doFind(self.find_text):
            pos = self.editor.get_pos()
            self.editor.set_selection(pos, pos-len(self.find_text))
        
    def findTextBackward(self):
        ans = appuifw2.query(u("Find backward"), "text", self.find_text)
        if ans is None: return
        self.find_text = ans
        if self.doFind(self.find_text, False):
            pos = self.editor.get_pos()
            self.editor.set_selection(pos, pos-len(self.find_text))
        
    def replaceText(self):
        ans = appuifw2.multi_query(u("Find"), u("Replace"))
        if ans is None: return
        self.find_text = ans[0]
        self.replace_text = ans[1]
        if self.doFind(self.find_text):
            self.doReplace(self.replace_text)
    
    def selectAll(self):
        self.editor.select_all()
        
    def selectNone(self):
        self.editor.clear_selection()
        
    def findEOL(self):
        self.doFind(u"\u2029")
    
    def cut(self):
        if self.editor.can_cut():
            self.editor.cut()
        else:
            appuifw2.note(u("Can't cut!"), "error")

    def copy(self):
        if self.editor.can_copy():
            self.editor.copy()
        else:
            appuifw2.note(u("Can't copy!"), "error")

    def paste(self):
        if self.editor.can_paste():
            self.editor.paste()
        else:
            appuifw2.note(u("Can't paste!"), "error")

    def undo(self):
        if self.editor.can_undo():
            self.editor.undo()
        else:
            appuifw2.note(u("Can't undo!"), "error")

class HTMLEditor(xText):
    '''HTML Editor. Uses appuifw2.Text
    '''
    version = VERSION
    title = u('HTML Editor %s' % (version))
    def __init__(self):
        xText.__init__(self)
    
    def quit(self):
        if self.notSaved():
            if not self.fileSave(): return
        self.app_lock.signal()
        appuifw2.app.set_exit()

    def aboutDlg(self):
        appuifw2.query(u('S60 HTML Editor\nVersion %s\nCopyright (c) Dmitri Brechalov, 2008' % (self.version)), 'query', ok=u(''), cancel=u('Close'))
        
    def helpDlg(self):
        topics = (u('Call button works as functional key.\nCall + arrows: Page Up, Page Down, Line Start and Line End.'),
                  u('Press Call + Select to go to the top/bottom of the text or goto line.'),
                  u('Press right softkey to select and insert HTML tag.\nSelect the same tag once more to insert close tag.'),
                  u('Select "Custom tag" to insert any tag.'),
                  u('Press Call + Right softkey to insert HTML entity.'),
                 )
        for t in topics:
            if not appuifw2.query(t, 'query', ok=u('Next'), cancel=u('Close')):
                break

    def fileDialog(self, allowNew=False):
        if allowNew:
            dirname = fileBrowser('Select directory', dironly=True)
            if dirname is None: return None
            ans = appuifw2.query(u('Type new file name:\n' + dirname), 'text')
            if ans:
                return os.path.join(dirname, s(ans))
            else:
                return None
        else:
            return fileBrowser('Select file')

    def fileNew(self):
        if self.notSaved():
            if not self.fileSave(): return
        self.editor.clear()
        appuifw2.app.title = self.title
        self.fname = None
        self.moveEvent()
        self.editor.has_changed = False

    def fileTemplate(self):
        if self.notSaved():
            if not self.fileSave(): return
        ans = appuifw2.popup_menu([u('Simple HTML'), u('HTML 4.01 Transitional')], u('Select template'))
        if ans is None: return
        self.fileNew()
        self.editor.set(u(htmltemplates[ans]))
        self.editor.set_pos(0)
        self.editor.has_changed = False
        
    def fileOpen(self):
        if self.notSaved():
            if not self.fileSave(): return
        ans = self.fileDialog()
        if not ans: return
        self.fname = ans
        appuifw2.app.title = u(os.path.split(self.fname)[1])
        try:
            self.editor.set(u(open(self.fname, 'r').read()))
            self.editor.set_pos(0)
            self.moveEvent()
            self.editor.has_changed = False
        except:
            appuifw2.note(u('Cannot read file %s!' % self.fname), 'error')
            self.fileNew()
    
    def doSave(self):
        try:
            open(self.fname, 'w').write(s(self.editor.get().replace(u"\u2029", u'\r\n')))
            self.editor.has_changed = False
            return True
        except:
            appuifw2.note(u('Cannot write file %s!' % self.fname), 'error')
            return False
    
    def fileSaveAs(self):
        ans = self.fileDialog(True)
        if not ans: return False
        self.fname = ans
        appuifw2.app.title = u(os.path.split(self.fname)[1])
        return self.doSave()
    
    def fileSave(self):
        if self.fname is None:
            return self.fileSaveAs()
        else:
            return self.doSave()

    def appendTag(self, tag, tags=None):
        if tags is None:
            self.editor.add(u('<%s/>' % tag))
        elif tag in tags:
            tags.remove(tag)
            self.editor.add(u('</%s>' % tag))
        else:
            tags.append(tag)
            self.editor.add(u('<%s>' % tag))
    
    def insertLink(self, anchor=False):
        if 'a' in self.tags:
            self.editor.add(u('</a>'))
            self.tags.remove('a')
        else:
            if anchor:
                op = 'name'
            else:
                op = 'href'
            self.editor.add(u('<a %s="">' % (op)))
            self.tags.append('a')
            
    def insertImage(self):
        self.editor.add(u('<img src=""/>'))

    def insertTag(self):
        tags = {'a href': self.insertLink,
                'a name': lambda : self.insertLink(True),
                'img': self.insertImage,
                'h': self.insertHeader,
                'strong': lambda : self.appendTag('strong', self.tags),
                'em': lambda : self.appendTag('em', self.tags),
                'code': lambda : self.appendTag('code', self.tags),
                'pre': lambda : self.appendTag('pre', self.tags),
                'u': lambda : self.appendTag('u', self.tags),
                'p': lambda : self.appendTag('p', self.tags),
                'ul': lambda : self.appendTag('ul', self.tags),
                'ol': lambda : self.appendTag('ol', self.tags),
                'li': lambda : self.appendTag('li', self.tags),
                's': lambda : self.appendTag('s', self.tags),
                'q': lambda : self.appendTag('q', self.tags),
                'blockquote': lambda : self.appendTag('blockquote', self.tags),
                'var': lambda : self.appendTag('var', self.tags),
                'tt': lambda : self.appendTag('tt', self.tags),
                'br': lambda : self.appendTag('br'),
                'hr': lambda : self.appendTag('hr'),
                }
        tlst = tags.keys()
        tlst.sort()
        ans = appuifw2.selection_list(map(u, ['Custom...'] + tlst), 1)
        if ans is None: return
        if ans == 0:
            self.insertCustomTag()
        else:
            tags[tlst[ans-1]]()

    def insertCustomTag(self):
        ans = appuifw2.query(u('HTML Tag:'), 'text')
        if not ans: return
        tag = s(ans).lower()
        self.appendTag(tag, self.tags)

    def insertEntity(self):
        ans = appuifw2.popup_menu(map(u, ('&', '<', '>', '"')))
        if ans is None: return
        self.addEntity(('amp', 'lt', 'gt', 'quot')[ans])

    def addEntity(self, ent):
        self.editor.add(u('&%s;' % ent))

    def insertHeader(self):
        if self.hdr is not None:
            self.editor.add(u('</h%s>' % self.hdr))
            self.hdr = None
        else:
            ans = appuifw2.popup_menu(map(u, ('H1', 'H2', 'H3', 'H4', 'H5', 'H6')))
            if ans is None: return
            self.hdr = ans + 1
            self.editor.add(u('<h%s>' % self.hdr))

    def launchBrowser(self):
        if self.notSaved():
            if not self.fileSave(): return
        appuifw2.Content_handler().open(u(self.fname.replace('/', '\\')))

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