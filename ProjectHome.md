**S60 HTML Editor** is a simple but useful editor for HTML code on Symbian smartphones.

Write and edit your HTML pages directly on your smartphone!

The main features include:
  * Easy insertion of HTML tags and entities using quick menu
  * Automatic control for the close tags (for tags such as `strong`, `em`, `a`, etc)
  * Fast moving through the text using hot keys and menus

The editor is written in Python using appuifw2 extension module.

The code was tested on _Nokia E51_ device and in S60 SDK emulator.

See [Manual](Manual.md) for details.

![http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainWindow.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainWindow.jpg)

## News ##

#### 2008-12-26 ####

  * Version 0.7 released
    * Tag insertion algorythm changed: inserts both open and close tags simultaneously, if needed, also asks for attributes as well. List of predefined tags extended.
    * View in browser option available.
    * Do not quit Python when runs as a script
    * Code has been refactored and improved.

#### 2008-12-23 ####

  * Version 0.6 released
    * SIS-file (unfortunately self-signed with test range UID, made by Ensymble)
    * The code refactored.

#### 2008-11-27 ####

  * Version 0.5 released
    * Cut/copy/paste in the menu
    * Undo works (but for cut/paste/delete selection operations)
    * Select all/none in the menu
    * Changes control fixed (the editor asks for save only if text has really been changed)

#### 2008-11-24 ####

  * Version 0.4 released:
    * more hot keys
    * position indicator
    * search forward/backward
    * Call + Right softkey inserts entities
    * Bugfixes: EOLN and replace

#### 2008-11-23 ####

  * SVN repository has been updated.
  * Manual for ver.0.3 has been published.
  * Issues have been added (for the next release).

#### 2008-11-22 ####

  * Version 0.3 released (hot keys, skinned editor, search improves)
  * Versions 0.1 and 0.2 released for historical reasons

#### 2008-11-20 ####

  * The project launched. Third beta released.