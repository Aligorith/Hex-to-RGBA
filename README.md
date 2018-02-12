Hex-to-RGBA
===========

Sublime Text 3 package for converting CSS hexadecimal colors to/from RGBA.

Installation
============

Install using [Package Control][1] or download/clone into your Sublime Text 3 package directory.

Usage
=====

** Hex to RGBA **
1. Select the hexadecimal value (e.g. `#ABCDEF` or `ABCDEF`)
2. Use the "Hex to RGBA" tool to convert this hex value to an equivalent RGBA representation (`r = 0-255, g = 0-255, b = 0-255, a = 0.0-1.0`)

** RGB(A) to Hex **
1. Select the RGB/RGBA function-call (e.g. `rgba(255, 125, 0, 0.5)`, or `rgb(0, 125, 255)`)
2. Use the "RGB(A) to Hex" tool to convert this rgba tuple to an equivalent Hex representation (`#RRGGBB`)


### Menu options
The tools can be accessed from the "Edit" > "Color Conversion Tools" submenu.


### Keyboard shortcuts

 OS     | Hex to RGBA  | RGB(A) to Hex
------- | :----------: | :------------:
Windows | Shift-Ctrl-R | Shift-Ctrl-H
Linux   | Shift-Ctrl-R | Shift-Ctrl-H
Mac     | Shift-Cmd-R  | Shift-Cmd-H

### Command Palette

The tools can be accessed from the command palette by searching for "hex" and selecting
either the "Convert: Hex to RGBA" or "Convert: RGB(A) to Hex" options as appropriate.


Credit
======

This package is a fork of the original ["Hex-to-RGBA" package][4] by [aroscoe][5].

[1]: http://wbond.net/sublime_packages/package_control
[2]: https://github.com/atadams/Hex-to-HSL-Color/
[3]: https://github.com/atadams/
[4]: https://github.com/aroscoe/Hex-to-RGBA
[5]: https://github.com/aroscoe

