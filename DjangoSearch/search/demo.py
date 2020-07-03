import xml.sax
import xml.sax.handler



class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping


data = '<?xml version="1.0" encoding="utf-8"?><SubmitResult xmlns="http://106.ihuyi.com/"><code>2</code><msg>提交成功</msg><smsid>15870246956696820530</smsid></SubmitResult>'

xh = XMLHandler()
xml.sax.parseString(data.encode(), xh)
ret = xh.getDict()
print(ret)