# Contents #



# About #

**S60 HTML Editor** is a simple text editor for _Symbian S60_ devices designed for editing HTML files. The major feature of the editor is fast and easy inserting HTML tags and entities.

The editor is written in **Python** programming language.

This manual describes version 0.7 of the editor.

Copyright (C) Dmitri Brechalov, 2008

# Requirements And Installation #

You **must** have [Python for S60](http://opensource.nokia.com/projects/pythonfors60/) installed on your device first.

You **must** have [appuifw2](http://code.google.com/p/appuifw2/) extension module installed on your device as well.

Currently the program is available as SIS-file and as source code. If you have S60 3rd Ed. device, you can install it from the SIS-file as a standalone application with own button in main menu.

Otherwise, you can simply copy the source code file to the `\Python` directory on the device or memory card (where Python is installed). Then start Python interpreter, press left softkey for the menu and select **Run script**. Select the scripts and press **OK**.

# Hot Keys #

The editor uses **Call** key as a functional key. Press:
  * **Call + Left key** to go to the  beginning of line;
  * **Call + Right key** to go to the end of line;
  * **Call + Up key** to page up;
  * **Call + Down** key to page down;
  * **Call + Select key** to open the quick move menu.

To insert any HTML tag press **Right softley**. Select a tag from tag menu or press **Custom...** and type your own.

# Main Menu #

Press **Options** to open the main menu.
  * **Insert tag** - Open tags menu. You can quickly insert any tag you want. See below for detail.
  * **Insert entity** - Open entities menu. You can quickly insert the most often HTML entities.
  * **Search** - Open find and replace menu:
    * **Find** - Find the first occurence of entered text. Search starts from current position of cursor.
    * **Find next** - Find the next occurence of the same text.
    * **Replace** - Find and replace the first occurence of the text with another text string.
  * **File** - File operations:
    * **Save** - Save the file. For new files asks for the file name and path.
    * **Save as** - Save the text in another file. Asks for the name and the path.
    * **Open** - Load file. The current text will be replaced with contents of selected file.
    * **New** - Drop all text and clear the editor.
    * **New from template** - You can select simple HTML and HTML 4.0 transitional templates for the new file.
    * **View in browser** - Open the file you edit in built-in browser.
  * **Help** - Short help.
    * **Help** - Display short help on the major functions of the editor.
    * **About** - Show copyright info.
  * **Exit** - Close the editor and return to OS.

# HTML Tag Insertion #

To insert an HTML tag press **Right softke** (labeled **Tag**), select a tag and press **OK**. To select a tag you can simply scroll the list, or start typing to quickly find the necessary tag. Also, you can use **Custom...** option - just type the tag you need and press **OK**. Some tags requires attributes (like `a` or `img`). You will be prompted for the names of attributes. Press **Cancel** when finished. The tag will be inserted to the text. It will have both open and close tags if needed.

Also you can select a text and insert tag using right softkey, selected text will be surrounded with selected tag.

That's all!

# Screenshots #

| ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainWindow.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainWindow.jpg) | ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainMenu.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/MainMenu.jpg) | ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/FileBrowser.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/FileBrowser.jpg) |
|:----------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| Main Window                                                                                                                                   | Main Menu                                                                                                                                 | File Browser                                                                                                                                    |
| ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/QuickMoveMenu.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/QuickMoveMenu.jpg) | ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/TagMenu.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/TagMenu.jpg)   | ![http://s60htmled.googlecode.com/svn/trunk/Screenshots/EntityMenu.jpg](http://s60htmled.googlecode.com/svn/trunk/Screenshots/EntityMenu.jpg)   |
| Quick Move Menu                                                                                                                               | Tag Selection Menu                                                                                                                        | Entity Selection Menu                                                                                                                           |