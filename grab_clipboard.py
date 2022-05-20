

import datetime
import card
import card_generator

from PIL import Image, ImageGrab
import uuid
import os
import io
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

import ctypes
import ctypes.wintypes as w
import codecs

import base64
import validators

"""Windows version of the grab_clipboard.py file"""
class ClipboardManager:

    def __init__(self, card_renderer, dao, uiStatus):  
        """
            The constructor for the ClipboardManager class.
        """
       
        self._timer = QTimer()  
        self.cardRenderer = card_renderer
        self.dao = dao
        self.oldCopy= None
        self._uiStatus = uiStatus


    def queryClipboard(self):
        """
            The function to check every 1.2 seconds if there is a new clipboard content and retrieves it.
            The function determines the type of the new clipboard content, stores it to the database, and
            depending on the currently selected category on the interface may create and display the card immediately.
            The bytes of each image are retrieved from the clipboard and stored as a png file in a folder in the same
            directory as the executable. The database stores the filepath.
        """
            
        
        cardId = uuid.uuid1().hex
        filename= "copied_image.png"
        copy1=None
        copy2 =None
        
        CF_UNICODETEXT = 13

        u32 = ctypes.WinDLL('user32')
        k32 = ctypes.WinDLL('kernel32')

        OpenClipboard = u32.OpenClipboard
        OpenClipboard.argtypes = w.HWND,
        OpenClipboard.restype = w.BOOL

        GetClipboardData = u32.GetClipboardData
        GetClipboardData.argtypes = w.UINT,
        GetClipboardData.restype = w.HANDLE

        EmptyClipboard = u32.EmptyClipboard
        EmptyClipboard.restype = w.BOOL

        SetClipboardData = u32.SetClipboardData
        SetClipboardData.argtypes = w.UINT, w.HANDLE,
        SetClipboardData.restype = w.HANDLE

        CloseClipboard = u32.CloseClipboard
        CloseClipboard.argtypes = None
        CloseClipboard.restype = w.BOOL

        GHND = 0x0042
        
        GlobalAlloc = k32.GlobalAlloc
        GlobalAlloc.argtypes = w.UINT, w.ctypes.c_size_t,
        GlobalAlloc.restype = w.HGLOBAL

        GlobalLock = k32.GlobalLock
        GlobalLock.argtypes = w.HGLOBAL,
        GlobalLock.restype = w.LPVOID

        GlobalUnlock = k32.GlobalUnlock
        GlobalUnlock.argtypes = w.HGLOBAL,
        GlobalUnlock.restype = w.BOOL

        GlobalSize = k32.GlobalSize
        GlobalSize.argtypes = w.HGLOBAL,
        GlobalSize.restype = w.ctypes.c_size_t
        
        unicode_type = type(u'')
        
        copy1 = None
        OpenClipboard(None)
        handle = GetClipboardData(CF_UNICODETEXT)
        pcontents = GlobalLock(handle)
        size = GlobalSize(handle)
        if pcontents and size:
            raw_data = ctypes.create_string_buffer(size)
            ctypes.memmove(raw_data, pcontents, size)
            copy1 = raw_data.raw.decode('utf-16le').rstrip(u'\0')
        GlobalUnlock(handle)
        CloseClipboard()
        
        if copy1==None:
            copy2 = ImageGrab.grabclipboard()
        if copy1!= self.oldCopy and isinstance(copy1,str) and copy1 and not copy1.isspace():
            self.oldCopy = copy1
            
            valid=validators.url(copy1)
            
            if valid:
                
                
                category ="URL"
                
                
            else:
                category = "Text"
                
            self.dao.storeCard(cardId, copy1, category, 0,0)
            if (self._uiStatus['ALL_STATE'] or (self._uiStatus['TEXT_STATE'] and category == 'Text')
                        or (self._uiStatus['URL_STATE'] and category == 'URL')):
                cardData = card.Card(cardId, copy1, category, 0,0)
                card_generator.CardObject(self.cardRenderer.parent, self.dao, self.cardRenderer).addToInterface(cardData)
                                                                               
                
                
         
        if copy2!=None and not isinstance(copy2,list):       
            if copy2!= Image.open(filename):
                
                
                copy2.save(filename,"PNG")
                filepath ="img_copy/" + str(uuid.uuid4()) + ".png"
               
                copy2.save(filepath,"PNG")
                pixmap = QPixmap(filepath)
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                category = "Image"
                self.dao.storeCard(cardId, filepath, category, 0, 0)

                if self._uiStatus['ALL_STATE'] or self._uiStatus['IMAGE_STATE']:
                    cardData = card.Card(cardId, filepath, category, 0, 0)
                    card_generator.CardObject(self.cardRenderer.parent, self.dao, self.cardRenderer).addToInterface(
                            cardData)
         

    def manageClip(self):
        """
            The function to retrieve the count of items in the clipboard every second.
            The function calls the updateUi function to update the interface every second.
        
        """
        try:
            self._timer.timeout.connect(lambda: self.queryClipboard())  
            self._timer.start(1200)  
        except:
            self._timer.timeout.connect(lambda: self.queryClipboard())  
            self._timer.start(7200)  
  



if __name__ == "__main__":
    gc = ClipboardManager()
    gc.manageClip()
