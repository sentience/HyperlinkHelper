import sublime, sublime_plugin
import re, urllib, urllib2
import os, sys
import chardet, pystache

def preemptive_imports():
	""" needed to ensure ability to import these classes later within functions, due to the way ST2 loads plug-in modules """
	from chardet import universaldetector
preemptive_imports()

class WrapSelectionAsLinkCommand(sublime_plugin.TextCommand):

	def get_url_title(self, url):
		try:
			req = urllib2.Request(url, headers={'User-Agent' : "Sublime Text 2 Hyperlink Helper"}) 
			f = urllib2.urlopen(req)
			url = f.geturl()
			content = f.read()
			decoded_content = content.decode(chardet.detect(content)['encoding'])
			title = re.search(r"<title>([^<>]*)</title>", decoded_content, re.I).group(1)
			title = title.strip()
			return title
		except Exception, e:
			sublime.error_message("Error fetching page title: %s" % str(e))
			return None

	def make_url(self, text):
		# convert email addresses to mailto: links
		match = re.match(r"^(mailto:)?(.*?@.*\..*)$", text)
		if match:
			return "mailto:%s" % match.group(2)
		else:
			# convert Amazon links (possibly containing affiliate codes) to canonical URLs
			match = re.match(r"^https?://www.(amazon.(?:com|co.uk|co.jp|ca|fr|de))/.+?/([A-Z0-9]{10})/[-a-zA-Z0-9_./%?=&]+$", text)
			if match: 
				return "http://%s/dp/%s" % (match.group(1), match.group(2))
			else:
				# pass through other URLs untouched
				match = re.match(r"^[a-zA-Z][a-zA-Z0-9.+-]*://.*$", text)
				if match:
					return text
				else:
					# add http:// protocol to URLs without them
					match = re.match(r"^(www\..*|.*\.(com|net|org|info|[a-z]{2}))$", text)
					if match:
						return "http://%s" % text
					else:
						# pass through non-whitespace text unmodified
						match = re.match(r"^\S+$", text)
						if match:
							return text
						else:
							return "http://example.com/"

	def run(self, edit):
		nonempty_sels = []

		# set aside nonempty selections
		for s in reversed(self.view.sel()):
			if not s.empty():
				nonempty_sels.append(s)
				self.view.sel().subtract(s)

		# expand remaining (empty) selections to words
		self.view.run_command("expand_selection", {"to": "word"})

		# add nonempty selections back in
		for s in nonempty_sels:
			self.view.sel().add(s)
		
		txt = sublime.get_clipboard().strip()
		url = self.make_url(txt)

		title = None
		if re.match(r"^https?://", url) and url != "http://example.com/":
			title = { 'title': self.get_url_title(url) }

		# apply the links
		old_sels = []
		for s in (self.view.sel()):
			old_sels.append(s)
		self.view.sel().clear()
		for s in reversed(old_sels):
			if not s.empty():
				txt = self.view.substr(s)
				link = pystache.render(self.view.settings().get('hyperlink_helper_link_format'), {'url': url, 'title?': title, 'input': txt})
				self.view.replace(edit, s, link)
				pos = s.begin() + len(link)
				self.view.sel().add(sublime.Region(pos, pos))
