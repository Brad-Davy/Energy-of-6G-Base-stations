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
        
    def test_rf_at_100_load(self):
        """
        Test that it can sum a list of integers
        """
        parameters = {'BW' : 10, 'Ant' : 4, 'M' :6, 'R' : 5/6, 'dt' : 99, 'df' : 100}
        baseBandPower, RFPower, PAPower, OHPower = returnTotalPower(parameters)
        self.assertEqual(int(RFPower), 40)    
        
    def test_bb_at_100_load(self):
        """
        Test that it can sum a list of integers
        """
        parameters = {'BW' : 10, 'Ant' : 4, 'M' :6, 'R' : 5/6, 'dt' : 99, 'df' : 100}
        baseBandPower, RFPower, PAPower, OHPower = returnTotalPower(parameters)
        self.assertEqual(int(baseBandPower), 81)   
    
    def test_pa_at_100_load(self):
        """
        Test that it can sum a list of integers
        """
        parameters = {'BW' : 10, 'Ant' : 4, 'M' :6, 'R' : 5/6, 'dt' : 99, 'df' : 100}
        baseBandPower, RFPower, PAPower, OHPower = returnTotalPower(parameters)
        self.assertEqual(int(PAPower), 759)  
        
    def test_oh_at_100_load(self):
        """
        Test that it can sum a list of integers
        """
        parameters = {'BW' : 10, 'Ant' : 4, 'M' :6, 'R' : 5/6, 'dt' : 99, 'df' : 100}
        baseBandPower, RFPower, PAPower, OHPower = returnTotalPower(parameters)
        self.assertEqual(int(OHPower), 249)  


if __name__ == '__main__':
    unittest.main()