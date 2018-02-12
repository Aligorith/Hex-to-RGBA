import re

import sublime
import sublime_plugin

class HexToRgbaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("Running hex2rgba")
        for selection in self.view.sel():
            print("  sel...")
            word_region = self.view.word(selection)
            print("word_region = %s" % (word_region))
            if not word_region.empty():
                word = self.view.substr(word_region)
                print("word = '%s'" % (word))
                start_idx = word_region.begin()
                while (len(word) > 0) and (word[0].isspace()):
                    word = word[1:]
                    start_idx += 1
                print("stripped word = '%s' (at %d)" % (word, start_idx))

                rgba_css = self.convert_to_rgba_css(word)
                if rgba_css:
                    print("rgba_css = '%s'" % (rgba_css))
                    if (word[0] != '#'):
                        tmp_region = sublime.Region(start_idx-1, word_region.end())
                        self.view.replace(edit, tmp_region, rgba_css)
                    else:
                        tmp_region = sublime.Region(start_idx, word_region.end())
                        self.view.replace(edit, tmp_region, rgba_css)
                else:
                    print("no rgba_css - '%s'" % (rgba_css))

    def hex_to_rgba(self, value):
        value = value.lower().lstrip('#')
        if len(value) == 3:
            value = ''.join([v*2 for v in list(value)])
        return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))+(1,)

    def convert_to_rgba_css(self, word):
        print("word substr = '%s'" % (word))
        re_hex_color = re.compile('\#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}')
        match_result = re_hex_color.match(word)
        print("--> match result = %s" % (match_result))
        if match_result:
            rgba = self.hex_to_rgba(word)
            rgba_css = 'rgba(%s,%s,%s,%s)' % rgba
            return rgba_css
        print("--> failed to match - %s" % (re_hex_color))
        return False
