from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label


class MyLabel(Image):
    text = StringProperty('')

    def on_text(self, *_):
        l = Label(text=self.text)
        l.font_size = '30dp'  
        l.texture_update()
        self.texture = l.texture

class Display(App):
    transactionHash=None
    blockNumber=None
    def setTransactionHash(self,transactionHash):
        self.transactionHash=transactionHash
    def setBlockNumber(self,blockNumber):
        self.blockNumber=blockNumber
    
    def build(self):
        return MyLabel(text='Transaction Hash:'+self.transactionHash+'\nBlock Number:'+self.blockNumber+'\n')


obj=Display()
obj.setBlockNumber("10")
obj.setTransactionHash("2")
obj.run()