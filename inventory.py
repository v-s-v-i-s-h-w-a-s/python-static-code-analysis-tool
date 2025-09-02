import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
import os

class InventoryManager:
    """A secure and robust inventory management system."""
    
    def __init__(self, log_file: str = "inventory.log"):
        self.stock_data: Dict[str, int] = {}
        self.logs: List[str] = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def add_item(self, item: str, qty: int) -> bool:
        """
        Add items to inventory with proper validation.
        
        Args:
            item: Item name (must be non-empty string)
            qty: Quantity to add (must be non-negative integer)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._validate_item_name(item):
            self.logger.error(f"Invalid item name: {item}")
            return False
        
        if not self._validate_quantity(qty):
            self.logger.error(f"Invalid quantity: {qty}")
            return False
        
        if qty < 0:
            self.logger.error(f"Cannot add negative quantity: {qty}")
            return False
        
        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        log_message = f"Added {qty} of {item}"
        self.logs.append(f"{datetime.now()}: {log_message}")
        self.logger.info(log_message)
        return True
    
    def remove_item(self, item: str, qty: int) -> bool:
        """
        Remove items from inventory with proper validation.
        
        Args:
            item: Item name
            qty: Quantity to remove (must be positive)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._validate_item_name(item):
            self.logger.error(f"Invalid item name: {item}")
            return False
        
        if not self._validate_quantity(qty):
            self.logger.error(f"Invalid quantity: {qty}")
            return False
        
        if qty <= 0:
            self.logger.error(f"Quantity to remove must be positive: {qty}")
            return False
        
        if item not in self.stock_data:
            self.logger.error(f"Item not found in inventory: {item}")
            return False
        
        if self.stock_data[item] < qty:
            self.logger.error(f"Insufficient stock for {item}. Available: {self.stock_data[item]}, Requested: {qty}")
            return False
        
        self.stock_data[item] -= qty
        if self.stock_data[item] == 0:
            del self.stock_data[item]
        
        log_message = f"Removed {qty} of {item}"
        self.logs.append(f"{datetime.now()}: {log_message}")
        self.logger.info(log_message)
        return True
    
    def get_quantity(self, item: str) -> Optional[int]:
        """
        Get quantity of an item in inventory.
        
        Args:
            item: Item name
        
        Returns:
            int: Quantity if item exists, None otherwise
        """
        if not self._validate_item_name(item):
            self.logger.error(f"Invalid item name: {item}")
            return None
        
        return self.stock_data.get(item, 0)
    
    def load_data(self, file_path: str = "inventory.json") -> bool:
        """
        Load inventory data from JSON file with proper error handling.
        
        Args:
            file_path: Path to JSON file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"File not found: {file_path}. Starting with empty inventory.")
                return True
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate loaded data
            if not isinstance(data, dict):
                self.logger.error("Invalid data format: expected dictionary")
                return False
            
            # Validate each item in loaded data
            validated_data = {}
            for item, qty in data.items():
                if self._validate_item_name(item) and self._validate_quantity(qty) and qty >= 0:
                    validated_data[item] = qty
                else:
                    self.logger.warning(f"Skipping invalid entry: {item} -> {qty}")
            
            self.stock_data = validated_data
            self.logger.info(f"Successfully loaded {len(self.stock_data)} items from {file_path}")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {file_path}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {e}")
            return False
    
    def save_data(self, file_path: str = "inventory.json") -> bool:
        """
        Save inventory data to JSON file with proper error handling.
        
        Args:
            file_path: Path to save JSON file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.stock_data, f, indent=2, sort_keys=True)
            
            self.logger.info(f"Successfully saved {len(self.stock_data)} items to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving data to {file_path}: {e}")
            return False
    
    def print_inventory(self) -> None:
        """Print current inventory in a formatted way."""
        print("\n" + "="*40)
        print("INVENTORY REPORT")
        print("="*40)
        
        if not self.stock_data:
            print("No items in inventory")
            return
        
        # Sort items alphabetically for consistent output
        for item in sorted(self.stock_data.keys()):
            print(f"{item:<20} -> {self.stock_data[item]:>5} units")
        
        print("="*40)
        print(f"Total unique items: {len(self.stock_data)}")
        total_units = sum(self.stock_data.values())
        print(f"Total units: {total_units}")
        print("="*40)
    
    def check_low_stock(self, threshold: int = 5) -> List[str]:
        """
        Find items with stock below threshold.
        
        Args:
            threshold: Minimum stock level
        
        Returns:
            List of item names with low stock
        """
        if not isinstance(threshold, int) or threshold < 0:
            self.logger.error(f"Invalid threshold: {threshold}")
            return []
        
        low_stock_items = []
        for item, qty in self.stock_data.items():
            if qty < threshold:
                low_stock_items.append(item)
        
        return sorted(low_stock_items)
    
    def get_logs(self) -> List[str]:
        """Get all operation logs."""
        return self.logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all operation logs."""
        self.logs.clear()
        self.logger.info("Operation logs cleared")
    
    def get_total_items(self) -> int:
        """Get total number of unique items."""
        return len(self.stock_data)
    
    def get_total_units(self) -> int:
        """Get total number of units across all items."""
        return sum(self.stock_data.values())
    
    def _validate_item_name(self, item: Union[str, None]) -> bool:
        """Validate item name."""
        return isinstance(item, str) and len(item.strip()) > 0
    
    def _validate_quantity(self, qty: Union[int, None]) -> bool:
        """Validate quantity."""
        return isinstance(qty, int)


def main():
    """Example usage of the InventoryManager."""
    # Create inventory manager
    inventory = InventoryManager()
    
    # Add items
    print("Adding items...")
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 5)
    inventory.add_item("orange", 3)
    
    # Try to add invalid items (should fail gracefully)
    inventory.add_item("", 5)  # Empty name
    inventory.add_item("grape", -2)  # Negative quantity
    inventory.add_item(123, 10)  # Invalid type for name
    inventory.add_item("cherry", "ten")  # Invalid type for quantity
    
    # Remove items
    print("\nRemoving items...")
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)
    
    # Try invalid removals
    inventory.remove_item("nonexistent", 1)  # Item doesn't exist
    inventory.remove_item("banana", 10)  # Not enough stock
    
    # Check quantities
    print(f"\nApple stock: {inventory.get_quantity('apple')}")
    print(f"Banana stock: {inventory.get_quantity('banana')}")
    
    # Check low stock items
    low_items = inventory.check_low_stock(threshold=5)
    print(f"Low stock items (threshold=5): {low_items}")
    
    # Print full inventory
    inventory.print_inventory()
    
    # Save and reload data
    print("\nSaving data...")
    inventory.save_data("test_inventory.json")
    
    print("Loading data...")
    new_inventory = InventoryManager()
    new_inventory.load_data("test_inventory.json")
    new_inventory.print_inventory()


if __name__ == "__main__":
    main()
