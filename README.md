Hex-to-RGBA
===========

Sublime Text 3 package for converting CSS hexadecimal colors to/from RGBA.

Installation
============

Download/clone into your Sublime Text 3 package directory.

This has only been tested with ST3 (build 3143). It may/may not be usable in ST2.


Usage
=====

###  Hex to RGBA
1. Select the hexadecimal value (e.g. `#ABCDEF` or `ABCDEF`)
2. Use the "Hex to RGBA" tool to convert this hex value to an equivalent RGBA representation 
  (`r = 0-255, g = 0-255, b = 0-255, a = 0.0-1.0`)

### RGB(A) to Hex
1. Select the RGB/RGBA function-call (e.g. `rgba(255, 125, 0, 0.5)`, or `rgb(0, 125, 255)`)
2. Use the "RGB(A) to Hex" tool to convert this rgba tuple to an equivalent Hex representation (`#RRGGBB`)

### Convert Color: 0-255 to Float
1. Select an RGB color value (expressed as an int from 0 to 255), not including whitespace or commas/parens.
2. Use the "Convert Color: 0-255 to Float" tool to convert this to a floating-point (0.0-1.0) representation of this value

### Convert Color: Float to 0-255
1. Select an RGB color value (expressed a float from 0.0 to 1.0), not including whitespace or commas/parens
2. Use the "Convert Color: Float to 0-255" tool to convert this to an 8-bit (0-255) value


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

This package is a fork of the original ["Hex-to-RGBA" package][4] by [aroscoe][5],
with substantial modifications by @Aligorith

[1]: http://wbond.net/sublime_packages/package_control
[2]: https://github.com/atadams/Hex-to-HSL-Color/
[3]: https://github.com/atadams/
[4]: https://github.com/aroscoe/Hex-to-RGBA
[5]: https://github.com/aroscoe

