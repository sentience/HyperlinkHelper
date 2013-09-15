ST Hyperlink Helper
===================

a port of [TextMate’s][tm] Hyperlink Helper bundle for [Sublime Text][st] (2 and 3)

What is this?
-------------

ST Hyperlink Helper is a collection of commands for the [Sublime Text][st] (2 and 3) text editor for Windows, OS X, and Linux. These commands make it super easy to insert hyperlinks into documents of various kinds using keyboard shortcuts.

Currently supported languages:

  * HTML
    * HTML in PHP
    * HTML (Django)
    * HTML (Rails)
    * HTML5
  * Markdown
  * Textile
  * LaTeX
  * DokuWiki (once Sublime Text 2 has a DokuWiki language file added to it)

Currently offered commands:

  * Link to Wikipedia Page for Selection
  * Lookup with Google & Link (Ctrl+Alt+Shift+L, ^⇧⌘L on Mac)
  * Wrap Word / Selection as Link (Ctrl+Alt+L, ^⇧L on Mac)

**Note:** You can also access these commands from the Command Palette (Ctrl+Shift+P, ⇧⌘P on Mac), which saves you having to remember the keyboard shortcuts.

Why is this needed?
-------------------

Hyperlink Helper is one of the most popular features of [TextMate][tm] a popular text editor for the Mac. In many ways, [Sublime Text 2][st2] is a superior editor to TextMate, but it lacks many of the convenience features that make TextMate so popular. This project is an effort to bring some of those features to Sublime Text 2.

How do I install this?
----------------------

The easiest way to install is to use [Package Control][pc].

Download the code for this project and drop it into a subdirectory of Sublime Text 2’s Packages folder. You can get to the Packages folder by choosing **Browse Packages…** from Sublime Text’s **Preferences** menu.

**Restart Sublime Text** if it is running to ensure the hyperlink templates are loaded.

Project Status
--------------

This project is **stable**, but is an incomplete port. The available functionality works and works well, but there are features of the original TextMate bundle that still need to be brought over.

[pc]: http://wbond.net/sublime_packages/package_control
[st]: http://www.sublimetext.com/
[tm]: http://macromates.com/
