"""@Package This is the main script which calls other scripts and also invoke Application 
QtGui.QApplication()

"""
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
import sys, serial,traceback,os,time
import numpy as np
from PyQt4.QtWebKit import *
import urllib2
from calculate import*
html = \
"""<!DOCTYPE html>
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
  </tr>
  <tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">4</td>
    <td class="tg-yw4l">45</td>
    <td class="tg-yw4l">23</td>
  </tr>
  <tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">32</td>
    <td class="tg-yw4l">12</td>
    <td class="tg-yw4l">44</td>
  </tr>
  <tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">5</td>
    <td class="tg-yw4l">76</td>
    <td class="tg-yw4l">88</td>
  </tr>
  <tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">21</td>
    <td class="tg-yw4l">33</td>
    <td class="tg-yw4l">41</td>
  </tr>
</table>
    <div id="map"></div>
    <script>
      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 42.232, lng: -83.7260},
		  
          zoom: 18
        });
		map.setMapTypeId('satellite');
      }
	  
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBoFC5IKNxwcYB5k7cm1l8aQqOi6HJiALI&callback=initMap"
    async defer></script>
  </body>
</html>
"""
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
    <th class="tg-yw4l">Latitude</th>
	<th class="tg-yw4l">Longitude</th>
    <th class="tg-yw4l">Time</th>
  </tr>"""
h2="""<tr>
        <TR ALIGN="CENTER">
    <td class="tg-yw4l">"""
h3="""</td>
    <td class="tg-yw4l">"""
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
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1000,700)
        self.center()
        self.setWindowTitle('Evigia Systems')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.statusBar().showMessage('Disconnected')
        self.createActions()
        self.html=html
        self.a=0b0000
        self.t=0
        self._vt1=1
        self._vt2=1
        self._vref=1
        self.uc=QtCore.Qt.Unchecked
        self.ch=QtCore.Qt.Checked
        self.setwin()
        self.CONNECTED=0
        self.anglee=30
        self.torque=0
        self.continue_samecomm=0
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20000)
        
    def setwin(self):
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QtGui.QGridLayout()
        
        """quit = QtGui.QPushButton('Close')
        tor = QtGui.QPushButton("Torque Sensor")
        quit.setGeometry(QtCore.QRect(10,10,70,40))
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        quit.setToolTip('Close')
        quit.setStyleSheet("background-image:url(:/images/save.png)")
        self.connect(quit,QtCore.SIGNAL( 'clicked()' ), QtGui.qApp,QtCore.SLOT( 'quit()'))
        self.layout.addWidget(quit,0,0)
        self.layout.addWidget(tor,0,1)"""
        self.layout.addWidget(self.Motorcontrol(), 1, 0)
        #self.widget.setStyleSheet("background-image:url(:/images/Back.png)")
        #self.Menu(self)
        self.statusbr(0)
        self.widget.setLayout(self.layout)
    def Motorcontrol(self):
		self.gps=QWebView()
		self.gps.setHtml(self.html)
		groupBox = QtGui.QGroupBox("Status Panel")
		groupBox.setFixedWidth(900)
		groupBox.setFixedHeight(600)
		vbox=QtGui.QVBoxLayout()
		vbox.addWidget(self.gps)
		groupBox.setLayout(vbox)
		return groupBox     
    def statusbr(self,d):
        if(d==0):
            self.statusBar().showMessage('Disconnected')
        else:
            self.statusBar().showMessage('Connected')
    def Menu(self,event):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Debug')
        fileMenu.addAction(self.conn)
        fileMenu.addAction(self.disconn)
        self.toolbar = self.addToolBar('Connect')
        self.toolbar.addAction(self.conn)
 
    def closeEvent(self, event):
        if(self.CONNECTED==1):
            reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you want to Disconnect and quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        else:
            event.accept()
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def createActions(self):
        self.conn = QtGui.QAction(QtGui.QIcon(':/images/download.jpg'),"&Connect", self,
                statusTip="Connect to a COM PORT", triggered=self.Connect)
        self.disconn = QtGui.QAction("&Disconnect", self,
                statusTip="Disconnect to a COM PORT", triggered=self.Disconnect)
    def Connect(self,event):
        self.connect_oikos()
        if self.c==1:
            self.statusbr(1)
            self.CONNECTED=1
    def Disconnect(self,event):
        self.ser.close()
        self.CONNECTED=0
        self.statusbr(0)
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def update(self):
		url=urllib2.urlopen("http://192.168.2.142:333",timeout=3)
		s=url.read()
		r=responses(s)
		h4=""
		for i in range(0,len(r)):
			h4=h4+h2
			for j in range(0,4):
				h4=h4+str(r[i][j])+h3
			h4=h4+"</td></tr>"
		h4=h4+"</table>"
		s=h6.replace("xx",str(r[0][2]))
		s=s.replace("yy",str(r[0][1]))
		h4=h4+s
		for i in range(0,len(r)):
			s=h7.replace("xx",str(r[i][2]))
			s=s.replace("yy",str(r[i][1]))
			h4=h4+s
		h4=h4+h8
		h=h1+h4+"</body></html>"
		self.html=h
		url.close()
		self.gps.setHtml(self.html)
		

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())        