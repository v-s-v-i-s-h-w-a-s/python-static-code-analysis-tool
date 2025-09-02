import unittest
import json
import os
import tempfile
import logging
from unittest.mock import patch, mock_open
import sys
import io

# Import the inventory module
from inventory import InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Comprehensive test suite for InventoryManager."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_inventory.json")
        self.test_log = os.path.join(self.test_dir, "test_inventory.log")
        
        # Create inventory manager for testing
        self.inventory = InventoryManager(log_file=self.test_log)
        
        # Suppress logging during tests
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Re-enable logging
        logging.disable(logging.NOTSET)
        
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_log):
            os.remove(self.test_log)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_add_item_valid(self):
        """Test adding valid items."""
        # Test adding new item
        result = self.inventory.add_item("apple", 10)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("apple"), 10)
        
        # Test adding to existing item
        result = self.inventory.add_item("apple", 5)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("apple"), 15)
        
        # Test adding zero quantity
        result = self.inventory.add_item("banana", 0)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("banana"), 0)
    
    def test_add_item_invalid(self):
        """Test adding invalid items."""
        # Test invalid item names
        self.assertFalse(self.inventory.add_item("", 10))  # Empty name
        self.assertFalse(self.inventory.add_item("   ", 10))  # Whitespace only
        self.assertFalse(self.inventory.add_item(None, 10))  # None
        self.assertFalse(self.inventory.add_item(123, 10))  # Number
        
        # Test invalid quantities
        self.assertFalse(self.inventory.add_item("apple", -5))  # Negative
        self.assertFalse(self.inventory.add_item("apple", "ten"))  # String
        self.assertFalse(self.inventory.add_item("apple", None))  # None
        self.assertFalse(self.inventory.add_item("apple", 3.14))  # Float
    
    def test_remove_item_valid(self):
        """Test removing valid items."""
        # Add items first
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 5)
        
        # Test removing partial quantity
        result = self.inventory.remove_item("apple", 3)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("apple"), 7)
        
        # Test removing all quantity (item should be deleted)
        result = self.inventory.remove_item("banana", 5)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("banana"), 0)
        self.assertNotIn("banana", self.inventory.stock_data)
    
    def test_remove_item_invalid(self):
        """Test removing invalid items."""
        self.inventory.add_item("apple", 5)
        
        # Test invalid item names
        self.assertFalse(self.inventory.remove_item("", 1))  # Empty name
        self.assertFalse(self.inventory.remove_item(None, 1))  # None
        self.assertFalse(self.inventory.remove_item(123, 1))  # Number
        
        # Test invalid quantities
        self.assertFalse(self.inventory.remove_item("apple", 0))  # Zero
        self.assertFalse(self.inventory.remove_item("apple", -1))  # Negative
        self.assertFalse(self.inventory.remove_item("apple", "one"))  # String
        
        # Test non-existent item
        self.assertFalse(self.inventory.remove_item("nonexistent", 1))
        
        # Test insufficient stock
        self.assertFalse(self.inventory.remove_item("apple", 10))  # Only 5 available
    
    def test_get_quantity(self):
        """Test getting item quantities."""
        # Test non-existent item
        self.assertEqual(self.inventory.get_quantity("nonexistent"), 0)
        
        # Test existing item
        self.inventory.add_item("apple", 10)
        self.assertEqual(self.inventory.get_quantity("apple"), 10)
        
        # Test invalid item names
        self.assertIsNone(self.inventory.get_quantity(""))
        self.assertIsNone(self.inventory.get_quantity(None))
        self.assertIsNone(self.inventory.get_quantity(123))
    
    def test_check_low_stock(self):
        """Test checking for low stock items."""
        # Add items with various quantities
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 3)
        self.inventory.add_item("cherry", 1)
        self.inventory.add_item("date", 7)
        
        # Test default threshold (5)
        low_items = self.inventory.check_low_stock()
        self.assertEqual(set(low_items), {"banana", "cherry"})
        
        # Test custom threshold
        low_items = self.inventory.check_low_stock(threshold=8)
        self.assertEqual(set(low_items), {"banana", "cherry", "date"})
        
        # Test threshold of 0
        low_items = self.inventory.check_low_stock(threshold=0)
        self.assertEqual(low_items, [])
        
        # Test invalid threshold
        result = self.inventory.check_low_stock(threshold="invalid")
        self.assertEqual(result, [])
        result = self.inventory.check_low_stock(threshold=-1)
        self.assertEqual(result, [])
    
    def test_save_and_load_data(self):
        """Test saving and loading inventory data."""
        # Add some items
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 5)
        
        # Save data
        result = self.inventory.save_data(self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Create new inventory and load data
        new_inventory = InventoryManager()
        result = new_inventory.load_data(self.test_file)
        self.assertTrue(result)
        
        # Verify data was loaded correctly
        self.assertEqual(new_inventory.get_quantity("apple"), 10)
        self.assertEqual(new_inventory.get_quantity("banana"), 5)
    
    def test_load_data_nonexistent_file(self):
        """Test loading from non-existent file."""
        result = self.inventory.load_data("nonexistent.json")
        self.assertTrue(result)  # Should succeed with empty inventory
        self.assertEqual(len(self.inventory.stock_data), 0)
    
    def test_load_data_invalid_json(self):
        """Test loading from file with invalid JSON."""
        # Create file with invalid JSON
        with open(self.test_file, 'w') as f:
            f.write("invalid json content")
        
        result = self.inventory.load_data(self.test_file)
        self.assertFalse(result)
    
    def test_load_data_invalid_format(self):
        """Test loading from file with invalid data format."""
        # Create file with valid JSON but wrong format
        with open(self.test_file, 'w') as f:
            json.dump(["not", "a", "dictionary"], f)
        
        result = self.inventory.load_data(self.test_file)
        self.assertFalse(result)
    
    def test_load_data_with_invalid_entries(self):
        """Test loading data with some invalid entries."""
        # Create file with mix of valid and invalid entries
        test_data = {
            "apple": 10,  # Valid
            "banana": 5,  # Valid
            123: 7,       # Invalid key type
            "cherry": "invalid",  # Invalid value type
            "date": -5,   # Invalid negative value
            "": 3         # Invalid empty key
        }
        
        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)
        
        result = self.inventory.load_data(self.test_file)
        self.assertTrue(result)  # Should succeed but skip invalid entries
        
        # Only valid entries should be loaded
        self.assertEqual(self.inventory.get_quantity("apple"), 10)
        self.assertEqual(self.inventory.get_quantity("banana"), 5)
        self.assertEqual(len(self.inventory.stock_data), 2)
    
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_save_data_io_error(self, mock_file):
        """Test save_data with IO error."""
        result = self.inventory.save_data(self.test_file)
        self.assertFalse(result)
    
    def test_print_inventory(self):
        """Test printing inventory."""
        # Test empty inventory
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.inventory.print_inventory()
            output = mock_stdout.getvalue()
            self.assertIn("No items in inventory", output)
        
        # Test inventory with items
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 5)
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.inventory.print_inventory()
            output = mock_stdout.getvalue()
            self.assertIn("apple", output)
            self.assertIn("banana", output)
            self.assertIn("Total unique items: 2", output)
            self.assertIn("Total units: 15", output)
    
    def test_get_total_items(self):
        """Test getting total number of unique items."""
        self.assertEqual(self.inventory.get_total_items(), 0)
        
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 5)
        self.assertEqual(self.inventory.get_total_items(), 2)
    
    def test_get_total_units(self):
        """Test getting total number of units."""
        self.assertEqual(self.inventory.get_total_units(), 0)
        
        self.inventory.add_item("apple", 10)
        self.inventory.add_item("banana", 5)
        self.assertEqual(self.inventory.get_total_units(), 15)
    
    def test_logs(self):
        """Test logging functionality."""
        # Initially no logs
        self.assertEqual(len(self.inventory.get_logs()), 0)
        
        # Perform operations
        self.inventory.add_item("apple", 10)
        self.inventory.remove_item("apple", 3)
        
        logs = self.inventory.get_logs()
        self.assertEqual(len(logs), 2)
        self.assertTrue(any("Added 10 of apple" in log for log in logs))
        self.assertTrue(any("Removed 3 of apple" in log for log in logs))
        
        # Clear logs
        self.inventory.clear_logs()
        self.assertEqual(len(self.inventory.get_logs()), 0)
    
    def test_edge_cases(self):
        """Test various edge cases."""
        # Very long item name
        long_name = "a" * 1000
        result = self.inventory.add_item(long_name, 1)
        self.assertTrue(result)
        
        # Very large quantity
        large_qty = 1000000
        result = self.inventory.add_item("bulk_item", large_qty)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity("bulk_item"), large_qty)
        
        # Unicode item names
        unicode_name = "🍎apple🍌"
        result = self.inventory.add_item(unicode_name, 5)
        self.assertTrue(result)
        self.assertEqual(self.inventory.get_quantity(unicode_name), 5)


class TestIntegration(unittest.TestCase):
    """Integration tests for the inventory system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.inventory_file = os.path.join(self.temp_dir, "integration_test.json")
        self.inventory = InventoryManager()
        
        # Suppress logging during tests
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        logging.disable(logging.NOTSET)
        
        if os.path.exists(self.inventory_file):
            os.remove(self.inventory_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_complete_workflow(self):
        """Test a complete inventory management workflow."""
        # Step 1: Add initial inventory
        items_to_add = [
            ("apple", 50),
            ("banana", 30),
            ("cherry", 20),
            ("date", 10),
            ("elderberry", 2)
        ]
        
        for item, qty in items_to_add:
            result = self.inventory.add_item(item, qty)
            self.assertTrue(result)
        
        # Step 2: Check initial state
        self.assertEqual(self.inventory.get_total_items(), 5)
        self.assertEqual(self.inventory.get_total_units(), 112)
        
        # Step 3: Process some orders (remove items)
        orders = [
            ("apple", 15),
            ("banana", 10),
            ("cherry", 5)
        ]
        
        for item, qty in orders:
            result = self.inventory.remove_item(item, qty)
            self.assertTrue(result)
        
        # Step 4: Check stock after orders
        self.assertEqual(self.inventory.get_quantity("apple"), 35)
        self.assertEqual(self.inventory.get_quantity("banana"), 20)
        self.assertEqual(self.inventory.get_quantity("cherry"), 15)
        
        # Step 5: Check for low stock items
        low_stock = self.inventory.check_low_stock(threshold=15)
        expected_low_stock = {"date", "elderberry"}
        self.assertEqual(set(low_stock), expected_low_stock)
        
        # Step 6: Restock low items
        restock = [
            ("date", 20),
            ("elderberry", 18)
        ]
        
        for item, qty in restock:
            result = self.inventory.add_item(item, qty)
            self.assertTrue(result)
        
        # Step 7: Save inventory
        result = self.inventory.save_data(self.inventory_file)
        self.assertTrue(result)
        
        # Step 8: Load inventory in new instance
        new_inventory = InventoryManager()
        result = new_inventory.load_data(self.inventory_file)
        self.assertTrue(result)
        
        # Step 9: Verify loaded data matches
        self.assertEqual(new_inventory.get_quantity("apple"), 35)
        self.assertEqual(new_inventory.get_quantity("banana"), 20)
        self.assertEqual(new_inventory.get_quantity("cherry"), 15)
        self.assertEqual(new_inventory.get_quantity("date"), 30)
        self.assertEqual(new_inventory.get_quantity("elderberry"), 20)
        
        # Step 10: Final verification
        self.assertEqual(new_inventory.get_total_items(), 5)
        final_low_stock = new_inventory.check_low_stock(threshold=15)
        self.assertEqual(final_low_stock, [])  # No low stock items


def run_tests():
    """Run all tests with detailed output."""
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestInventoryManager))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
