import urllib.request as urllib2
import html2text
import re

html = str(urllib2.urlopen("URL HERE").read())

h = html2text.HTML2Text()
text = re.sub(r'\\x[0-9a-f][0-9a-f]', '', h.handle(html))
texts = re.findall(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", text)

for i in range(0, len(texts)):
    texts[i] = texts[i].split(":")[0]

for i in range(0, len(texts)):
    print(texts[i])
