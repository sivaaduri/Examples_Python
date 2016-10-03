import urllib2
import re
response = urllib2.urlopen("http://192.168.2.142:333",timeout=3).read()
s=response
regex=r"({[\w,?;]+})"
if re.search(regex,s):
	match = re.findall(regex, s)
	print match[0]
	#print match.group(1)
	regex1 = r"([\w]+,)"
	val = re.findall(regex1,match[0])
	g=[]
	for values in val:
		values=values.replace(",","")
		print values
		g.append(int(values))