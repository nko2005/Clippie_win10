import sqlite3
import unittest
from dao import*
import clipboardManager_DB
import uuid 
import os

""" Unit testing class for the database user"""

class TestDb(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """This function setups are test of the db by initliazing the db creating a user """
        
        
       
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
    
        
    @classmethod
    def tearDownClass(cls):
        
        
        db.resetDb()
        #checking if file exist or not
        if(os.path.isfile("ClipboardManager_DB.db")):
            #os.remove() function to remove the file
            os.remove("ClipboardManager_DB.db")
            #Printing the confirmation message of deletion
            print("File Deleted successfully")
        else:
            print("File does not exist")
            #Showing the message instead of throwig an error
        
    
    """Test Case"""
    
    def testChangeStateThenChangePassword(self):
        """Tests the setPasswordState() and changePassword() and getPassword()  """
        
        db.setPasswordState(1)
        db.changePassword("Test")
        result = db.getPassword()
        
        self.assertEqual(result,"Test")
        
        
     
        
   
    
        

if __name__ == "__main__":
    
    unittest.main()
     
     
     
     
     
     

