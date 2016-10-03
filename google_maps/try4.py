import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


js = \
"""
QFile = function(path)
{
    var name = _QFile_factory.createQFile(path);
    document.getElementById("name").innerText = name;
    return _wrapper;
}
"""

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
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 42.231664, lng: -83.725978},
          zoom: 20
        });
      }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB7yReQDjAR4t7XCixGNzpBO-vva5gDzpw&callback=initMap"
    async defer></script>
  </body>
</html>
"""

class FileWrapper(QObject):

    def __init__(self, path):
    
        QObject.__init__(self)
        self.file = QFile(path)
    
    @pyqtSignature("open(int)")
    def open(self, flags):
    
        return self.file.open(QIODevice.OpenModeFlag(flags))
    
    def readAll(self):
    
        return str(self.file.readAll())
    
    readAll = pyqtProperty("QString", readAll)
    
    @pyqtSignature("close()")
    def close(self):
    
        self.file.close()

class Browser(QWebView):

    def __init__(self, parent = None):
    
        QWebView.__init__(self, parent)
        self.connect(self, SIGNAL("loadFinished(bool)"), self.prepareJavaScript)
    
    def prepareJavaScript(self, ready):
    
        if not ready:
            return
        
        self.page().mainFrame().addToJavaScriptWindowObject("_QFile_factory", self)
        self.page().mainFrame().evaluateJavaScript(js)
    
    @pyqtSignature("createQFile(QString)")
    def createQFile(self, path):
    
        self.page().mainFrame().addToJavaScriptWindowObject("_wrapper", FileWrapper(path))
        return "_wrapper"


if __name__ == "__main__":

    app = QApplication(sys.argv)
    browser = Browser()
    browser.setHtml(html)
    browser.show()
    sys.exit(app.exec_())