import re
s="dd2,{35ee7d;195,98,117,16,195,184,151,32,03,158,02,00,01,00,00,00,},{35eef3;07,55,117,16,164,224,151,32,03,158,02,00,14,00,00,00,}dd"
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