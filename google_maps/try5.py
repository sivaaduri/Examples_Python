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
<body>
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;margin:0px auto;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:13px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:13px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
.tg .tg-yw4l{vertical-align:top}
</style>
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
<img src="https:maps.googleapis.com/maps/api/staticmap?center=42.2321,-83.7260&zoom=18&size=400x400&maptype=hybrid&markers=color:blue%7Clabel:ff%7C42.231664,-83.725978
&key=AIzaSyBoFC5IKNxwcYB5k7cm1l8aQqOi6HJiALI" height="500" width="500">


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