import re

import sublime
import sublime_plugin

class HexToRgbaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in self.view.sel():
			word_region = self.view.word(selection)
			if not word_region.empty():
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
