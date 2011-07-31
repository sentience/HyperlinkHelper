import sublime, sublime_plugin

def clamp(xmin, x, xmax):
    if x < xmin:
        return xmin
    if x > xmax:
        return xmax
    return x;

def classify(char, charsets):
    if len(char) == 0:
        return -2

    for i in xrange(0, len(charsets)):
        if char in charsets[i]:
            return i
    return -1

class LookupWithGoogleAndLink(sublime_plugin.TextCommand):

	def expand_to_word(self, view, pos):
		line = view.line(pos)

		classes = [" \t", view.settings().get("word_separators"), "\n"]
		# 1) look for first non-word character before pos in the line
		while pos > line.a and classify(view.substr(sublime.Region(pos, pos - 1)), classes) == -1:
			pos -= 1

		# 2) if it's followed by one or more word characters,
		#    return a selection containing them
		if classify(view.substr(sublime.Region(pos, pos + 1)), classes) == -1:
			pos2 = pos + 1
			while classify(view.substr(sublime.Region(pos2, pos2 + 1)), classes) == -1:
				pos2 += 1
			return sublime.Region(pos, pos2)

		# 3) if not, return empty selection
		return sublime.Region(pos, pos)

	def run(self, edit):
		new_sels = []

		# expand each selected region that is empty to encompass
		# the nearest word
		for s in reversed(self.view.sel()):
			if s.empty():
				new_sels.append(self.expand_to_word(self.view, s.b))
		
		# add the new selections to the document (clamped to
		# document limits - TODO: is this needed?)
		sz = self.view.size()
		for s in new_sels:
			self.view.sel().add(sublime.Region(clamp(0, s.a, sz),
				clamp(0, s.b, sz)))

		# apply the links
