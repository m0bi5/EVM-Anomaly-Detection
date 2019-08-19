from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
import time

change=False
class Display(App):
    transactionHash=None
    label=None
    def setTransactionHash(self,transactionHash):
        self.transactionHash=transactionHash
    def build(self):
        self.text="""
                                     [size=50]Vote Casted![/size]
        \n\n\n\n\n\n\n\n\n\n\n\n
                                              [size=24]Transaction Hash[/size]
                                              ------------------------------------------------
        \n
        """
        self.label=Label(text=text+self.transactionHash,markup=True)
        return self.label


obj=Display()
obj.setTransactionHash("0x80f34fa5e8c9047d8abf07b32fad091b9f2633b86400318aea04251b53def589")
obj.run()
