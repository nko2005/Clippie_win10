
import sqlite3
import unittest
from dao import*
import clipboardManager_DB
import uuid 
import os

""" Unit testing class for the database"""

class TestDb(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        This function sets up test of the db by initliazing the db creating a user record, and creating some card records once before
        all test cases
        """
        
        
       
        conn = sqlite3.connect('ClipboardManager_DB.db')
        cursor = conn.cursor()
        """
        Initially creates the database and all the tables.

        """

        
        CREATE_CARD_ENTITY = """
            CREATE TABLE IF NOT EXISTS card(
                cardID TEXT not null,
                cardContent TEXT not null,
                cardCategory TEXT not null,
                hideCard INTEGER not null,
                favoriteCard INTEGER not null
            );"""

        CREATE_USER_ENTITY = """
            CREATE TABLE IF NOT EXISTS user(
                userID INTEGER primary key,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                passwordExists BOOLEAN NOT NULL
            );"""
        cursor.execute(CREATE_CARD_ENTITY)
        cursor.execute(CREATE_USER_ENTITY)
        cls.userEmail = "test@gmail.com"
        
        clipboardManager_DB.createUser(cls.userEmail)
        
        cls.cardData1 = [str(uuid.uuid4()),"Hello_world", "Text", 0,1]
        cls.cardData2 = [str(uuid.uuid4()),"https://www.youtube.com", "URL", 1,0]
        cls.cardData3 = [str(uuid.uuid4()),str(uuid.uuid4()), "Image", 0,0]
        
        clipboardManager_DB.addCard(cls.cardData1[0], cls.cardData1[1], cls.cardData1[2], cls.cardData1[3], cls.cardData1[4])
        clipboardManager_DB.addCard(cls.cardData2[0], cls.cardData2[1], cls.cardData2[2], cls.cardData2[3], cls.cardData2[4])
        clipboardManager_DB.addCard(cls.cardData3[0], cls.cardData3[1], cls.cardData3[2], cls.cardData3[3], cls.cardData3[4])
    @classmethod
    def tearDownClass(cls):
        """
        This function empties the database then deletes the ClipboardManager_DB.db file after all test cases are done
        """

    
        
        
        db.resetDb()
        
        if(os.path.isfile("ClipboardManager_DB.db")):
            
            os.remove("ClipboardManager_DB.db")
            
            print("File Deleted successfully")
        else:
            print("File does not exist")
            
        
    
    """Test Cases"""
    
    def testGetAllCards(self):
        """Tests the db getAllCards() function """
        
        cards = clipboardManager_DB.getAllCards()
        
        print(cards)
        
    def testGetTextCards(self):
         """Tests the db getTextCards() function """
         
         result = db.getTextCards()
         
         self.assertEqual(result[0][1],self.cardData1[1])
        
    def testGetImageCards(self):
        """Tests the db getImageCards() function """
        
        result = db.getImageCards()
        
        self.assertEqual(result[0][1],self.cardData3[1])
        
    def testGetUrlCards(self):
        """Tests the db getUrlCards() function """
        
        result = db.getUrlCards()
        
        self.assertEqual(result[0][1],self.cardData2[1])
        
    def testGetSearchCards(self):
        """Tests the db getSearchCards(search) function """
        
        result = db.getSearchCards("Hello")
        
        self.assertEqual(result[0][1],self.cardData1[1])
        
        
    def testGetFavoriteCards(self):
        """Tests the getFavoriteCards() function """
        result = db.getFavoriteCards()
        
        self.assertEqual(result[0][1],self.cardData1[1])
        
        
        
    def testHidCard(self):
        """Tests the hideCard() function """
        db.hideCard(1,self.cardData3[0])
        result = db.getImageCards()
        self.assertEqual(result[0][3],True)
        
    def testfavoriteCard(self):
        """Tests the favoriteCard() function """
        db.favoriteCard(1,self.cardData3[0])
        result = db.getImageCards()
        self.assertEqual(result[0][4],True)
    
    
        
        
    def testGetEmail(self):
        """ Tests the getEmail() function"""
        
        result = db.getEmail()
        self.assertEqual(result,self.userEmail)
        
    def testGetPasswordState(self):
        """ Tests getPasswordState function"""
        
        result = db.getPasswordState()
        self.assertEqual(result,0)
         
    
        

if __name__ == "__main__":
    
    unittest.main()
     
     
     
     
     
     

