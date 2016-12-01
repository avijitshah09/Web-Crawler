from goose import Goose
import urllib2

url = "http://web2.uvcs.uvic.ca/courses/elc/studyzone/200/reading/vals-garden1.htm"
#try when something not working
"""opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
response = opener.open(url)
raw_html = response.read()
g = Goose({'browser_user_agent': 'Magic Browser', 'parser_class':'soup'})
page = g.extract(raw_html=raw_html)"""
g = Goose()
page = g.extract(url)
title_by_goose = page.title
story = page.cleaned_text
print "title:",' '.join(title_by_goose.split(' ')[1:])
print "story:", story
print "additional data:", page.additional_data
print "authors:", page.authors
print "infos", page.infos
print "meta_description", page.meta_description
print "meta_favicon",page.meta_favicon
print "meta_keywords", page.meta_keywords
print "meta_lang", page.meta_lang
print "opengraph", page.opengraph
print "publish_date", page.publish_date
print "tweets", page.tweets
print "domain", page.domain

