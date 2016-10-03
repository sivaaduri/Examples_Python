import urllib2
urllib2.urlopen("http://online-live1.services.u-blox.com/GetOnlineData.ashx?token= XXXXXXXXX;gnss=gps,glo;datatype=eph").read()