from card import *

import unittest

class TestCard(unittest.TestCase):
    """ test class for the card class"""
    
    def setUp(self):
        """initalizes card objects"""
        
        self.card1 = Card("text","hello")      
        self.card2 = Card("hyperlink","www.google.com")
        self.card3 = Card("image", "JGkemqn&302832Jfkm")
 
    
    def test_ID(self):
        """Tests card ID unqiueness"""
        
        self.assertNotEqual(self.card1.getId(),self.card2.getId())
        
        
        
    def test_cardContent(self):
        """Test if card content type is str"""
        
        self.assertIsInstance(self.card1.getContent(),str)
        
        
    def test_cardLabel(self):
        """Test if card label type is str"""
        self.assertIsInstance(self.card1.getCategory(),str)
        
        
    def test_setCardContent(self):
        """Tests input validation for setting card content"""
        with self.assertRaises(Exception):
            self.card1.setContent(500)
            
            
            
    def test_setCategory(self):
        """Tests input validation for setting card label
        raieses exception when setting cardLabel type to bool"""
        with self.assertRaises(Exception):
            
            self.card1.setCategory(True)
    
if __name__ == "__main__":
    
    unittest.main()