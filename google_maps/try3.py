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
"""<html>
<body>

<iframe src="https://www.google.com/maps/embed/v1/place?key=AIzaSyB7yReQDjAR4t7XCixGNzpBO-vva5gDzpw
  &q=Fairmont+Empress,Victoria+BC
  &attribution_source=Google+Maps+Embed+API
  &attribution_web_url=http://www.fairmont.com/empress-victoria/
  &attribution_ios_deep_link_id=comgooglemaps://?daddr=Fairmont+Empress,+Victoria,+BC" height="500" width="500"></iframe>


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