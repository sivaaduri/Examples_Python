import re
s="dd2,{35ee7d;195,98,117,16,195,184,151,32,03,158,02,00,01,00,00,00,},{35eef3;07,55,117,16,164,224,151,32,03,158,02,00,14,00,00,00,}dd"
regex=r"({[\w,?;]+})"

def unpack(arr,s):
	arr_m= (arr[5]<<24) | (arr[4]<<16) | (arr[1]<<8) | arr[0]
	arr_ab= arr[3]<<8 | arr[2]
	temp=arr_m
	div=1.0
	while(temp>1):
		temp=temp/10
		div=div*10
	arr_v=int(arr_ab/100)+(arr_ab%100+arr_m/div)/60.0
	if(s is "S" or s is "W"):
		arr_v=arr_v*-1.0
	return arr_v
def unpack_int(arr):
	return (arr[3]<<24) | (arr[2]<<16) | (arr[1]<<8) | arr[0]

def responses(res):
	s=res
	print s
	num=int(s[2])
	w, h = 4, num 
	result = [[0 for x in range(w)] for y in range(h)] 
	if re.search(regex,s):
		match = re.findall(regex, s)
		#print match[0]
		#print match.group(1)
		regex1 = r"([\w]+,)"
		regex2 = r"([\w]+;)"
		for I in range(0,num):
			val = re.findall(regex1,match[I])
			g=[]
			for values in val:
				values=values.replace(",","")
				#print values
				g.append(int(values))
			lat_a=[]
			long_a=[]
			time_a=[]
			for i in range(0,4):
				lat_a.append(g[i])
			for i in range(4,8):
				long_a.append(g[i])
			lat_a.append(g[12])
			lat_a.append(g[13])
			long_a.append(g[14])
			long_a.append(g[15])
			for i in range(8,12):
				time_a.append(g[i])
			#uint32_t r = (((uint32_t)num5<<24 )|((uint32_t)num4<<16)|((uint32_t)num1<<8 )|((uint32_t)num0));
			#uint32_t l = (uint32_t)num3<<8 | (uint32_t)num2;
			#return (num[0] | (uint32_t)num[1]<<8 | (uint32_t)num[2]<<16 | (uint32_t)num[3]<<24);
			lat=unpack(long_a,"W")
			long=unpack(lat_a,"N")
			time=unpack_int(time_a)
			ser=re.findall(regex2,match[I])
			ser[0]=ser[0].replace(";","")
			result[I][0]=(ser[0])
			result[I][1]=(lat)
			result[I][2]=(long)
			result[I][3]=(time)
			print long,lat,time,ser[0]
	return result
	