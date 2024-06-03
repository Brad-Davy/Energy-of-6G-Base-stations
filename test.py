import unittest
from energyConsumption import *



class TestSum(unittest.TestCase):
    
    
    def test_rf_component_values_receiver(self):
        """
        Test that it can sum a list of integers
        """
        receiver_values = sum(RF_COMPONENT_POWER_RECEIVER.values())
        self.assertEqual(receiver_values, 5140)
        
        
    def test_rf_component_values_transmitter(self):
        """
        Test that it can sum a list of integers
        """
        receiver_values = sum(RF_COMPONENT_POWER_TRANSMITTER.values())
        self.assertEqual(receiver_values, 5740)
        
    

if __name__ == '__main__':
    unittest.main()