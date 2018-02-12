import re

import sublime
import sublime_plugin


####################################
# Regex Expressions

# Compile the regex expressions once on load, instead of everytime we use the operators
# - Match hex-color
re_hex_color = re.compile('\#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}')

# - Match rgb(a)
re_rgba_color = re.compile(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)")
re_rgb_color = re.compile(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)")

####################################
# Conversion Routines

# Convert from 0-1 (float) to 0-255 (byte) value
# < float_value: (float [0.0, 1.0])
# > returns: (int [0, 255]) 
def float_to_byte(float_value):
	# Sanity checks
	if float_value == 0:
		return 0
	elif float_value == 1:
		return 255
	elif not type(float_value) is float:
		raise TypeError("'float_value' should be a float (got %s instead)" % (type(float_value)))
	
	# Ensure value is between acceptable limits
	# TODO: Just clamp instead?
	if 0 <= float_value <= 1:
		return int(float_value * 255.0)
	else:
		raise ValueError("'float_value' should be between 0.0 and 1.0 inclusive (got %.3f instead)" % (float_value))


# Convert from 0-255 (byte) to 0-1 (float)
# < byte_value: (int [0, 255])
# > returns: (float [0.0, 1.0])
def byte_to_float(byte_value):
	if type(byte_value) is not int:
		raise TypeError("'byte_value' should be an int between 0-255 inclusive (got %s instead)" % (byte_value))
	
	if 0 <= byte_value <= 255:
		return byte_value / 255.0
	else:
		raise ValueError("'byte_value' should be an int between 0-255 inclusive (got %s instead)" % (byte_value))


# Convert from 0-255 value to a 2-letter hexcode
def byte_to_hex(str_value, use_fixed_width=True):
	# Note: This assumes that we're dealing with the 0-255 version (not 0.0-1.0 floats)
	value = int(str_value)
	assert(0 <= value <= 255)
	
	# 1) hex() adds "0x" to the strings, so we must strip that
	# 2) hex() output is lowercase... assume that we want uppercase only
	hex_value = hex(value)[2:].upper()
	
	# Pad the output to ensure we get 2 digits always (otherwise a single digit may screw things up)
	if use_fixed_width: 
		return "{0: >2s}".format(hex_value)
	else:
		return hex_value


####################################

class HexToRgbaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in self.view.sel():
			word_region = self.view.word(selection)
			if not word_region.empty():
				# Strip whitespace at start of selection, or else checks for '#' fail
				word = self.view.substr(word_region)
				start_idx = word_region.begin()
				while (len(word) > 0) and (word[0].isspace()):
					word = word[1:]
					start_idx += 1
				
				rgba_css = self.convert_to_rgba_css(word)
				if rgba_css:
					if (word[0] != '#'):
						tmp_region = sublime.Region(start_idx-1, word_region.end())
						self.view.replace(edit, tmp_region, rgba_css)
					else:
						tmp_region = sublime.Region(start_idx, word_region.end())
						self.view.replace(edit, tmp_region, rgba_css)
	
	def hex_to_rgba(self, value):
		value = value.lower().lstrip('#')
		if len(value) == 3:
			value = ''.join([v*2 for v in list(value)])
		return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))+(1,)
	
	def convert_to_rgba_css(self, word):
		global re_hex_color
		match_result = re_hex_color.match(word)
		if match_result:
			rgba = self.hex_to_rgba(word)
			rgba_css = 'rgba(%s,%s,%s,%s)' % rgba
			return rgba_css
		return False


class RgbaToHexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in reversed(self.view.sel()):
			text = self.view.substr(selection)
			
			# TODO: Preserve extra whitespace, instead of just truncating and replacing
			text = text.strip()
			
			if text.startswith("rgba("):
				global re_rgba_color
				match = re_rgba_color.match(text)
			elif text.startswith("rgb("):
				global re_rgb_color
				match = re_rgb_color.match(text)
			else:
				match = None
			
			if match:
				# Extract the components
				r = match.group(1)
				g = match.group(2)
				b = match.group(3)
				#a = match.group(4) # XXX: This cannot be converted in most cases
				
				# Convert and replace
				hex_str = self.rgb_to_hex__bytes(r, g, b)
				self.view.replace(edit, selection, hex_str)
	
	def rgb_to_hex__bytes(self, r, g, b):
		hex_codes = [byte_to_hex(v) for v in (r, g, b)]
		return "#%s%s%s" % (hex_codes[0], hex_codes[1], hex_codes[2])


class RgbaByteToFloatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in reversed(self.view.sel()):
			# TODO: Preserve extra whitespace of just truncating and replacing
			text = self.view.substr(selection)
			text = text.strip()
			
			# String to "byte" int (i.e. 0-255 value)
			if text.isdigit():
				byte_value = int(text)
				if 0 <= byte_value <= 255:
					# Convert and replace
					float_value = str(byte_to_float(byte_value))
					self.view.replace(edit, selection, float_value)


class RgbaFloatToByteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in reversed(self.view.sel()):
			# TODO: Preserve extra whitespace of just truncating and replacing
			text = self.view.substr(selection)
			text = text.strip()
			
			# Try to convert "float-string" to byte-value
			# TODO: This needs a precision setting...
			try:
				float_value = float(text)
				byte_value  = str(float_to_byte(float_value))
				self.view.replace(edit, selection, byte_value)
			except Exception as e:
				print("ERROR %s: %s" % (type(e), e))

