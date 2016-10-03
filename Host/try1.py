from calculate import*
import numpy as np
s="dd2,{35ee7d;195,98,117,16,195,184,151,32,03,158,02,00,01,00,00,00,},{35ee83;07,55,117,16,164,224,151,32,03,158,02,00,14,00,00,00,}dd"
r=responses(s)
h1="""<!DOCTYPE html>
<html>
  <head>
    <title>Simple Map</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
		.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;margin:0px auto;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:13px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:13px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
.tg .tg-yw4l{vertical-align:top}
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
  <table class="tg">
        <TR>
         <H3><BR><center>Evigia</center></H3>
    <tr>
  <tr>
        <TR ALIGN="CENTER">
    <th class="tg-031e">Tag ID</th>
    <th class="tg-yw4l">GPS Coordinates</th>
    <th class="tg-yw4l">Time</th>
  </tr>"""
r=np.array(r)
h2="""<tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">"""
h3="""</td>
    <td class="tg-yw4l">"""
h4=""
for i in range(0,len(r)):
	h4=h4+h2
	for j in range(0,4):
		h4=h4+str(r[i][j])+h3
	h4=h4+"</td></tr>"
h4=h4+"</table>"
h6="""<div id="map"></div>
    <script>
      var map;
      function initMap() {
	  var bangalore = {lat: 42.232, lng: -83.7260};
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: xx, lng: yy},
		  
          zoom: 18
        });"""
h7="""var marker = new google.maps.Marker({
          position: {lat: xx, lng: yy},
          map: map,
		  title: 'Uluru (Ayers Rock)'
        });"""
h8="""map.setMapTypeId('satellite');
      }
	  
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBoFC5IKNxwcYB5k7cm1l8aQqOi6HJiALI&callback=initMap"
    async defer></script>"""
h5="</body></html>"
h=h1+h4