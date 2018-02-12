import re

import sublime
import sublime_plugin

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
		re_hex_color = re.compile('\#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}')
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
			
			# TODO: Precompile the regex objects once
			if text.startswith("rgba("):
				re_rgba_color = re.compile(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)")
				match = re_rgba_color.match(text)
			elif text.startswith("rgb("):
				re_rgb_color = re.compile(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)")
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
		# XXX: Assumes the 0-255 version (not 0.0-1.0 floats)
		# XXX: Assumes that we want uppercase only
		def int_to_hex(value):
			# 1) hex() adds "0x" to the strings, so we must strip that
			# 2) hex() output is lowercase... we want upper
			return hex(int(value))[2:].upper()
		
		hex_codes = [int_to_hex(v) for v in (r, g, b)]
		return "#%s%s%s" % (hex_codes[0], hex_codes[1], hex_codes[2])

