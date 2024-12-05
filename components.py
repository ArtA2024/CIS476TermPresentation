# components.py

# Component to represent the Vault View (e.g., the table showing items)
from mediators import Mediator

class VaultView:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def refresh(self, vault_items):
        # Logic to refresh the view based on new vault items
        print("Vault view refreshed with items:", vault_items)



# Component to handle adding, updating, and deleting vault items
class VaultForm:
    def __init__(self, mediator):
        self.mediator = mediator

    # Add a new item
    def add_item(self, item_data: dict):
        # Logic to add the item to the database
        print("Item Added:", item_data)
        # Notify the mediator
        self.mediator.notify(self, "item_added", item_data)

    # Update an existing item
    def update_item(self, item_id: int, item_data: dict):
        # Logic to update the item in the database
        print(f"Item with ID {item_id} Updated:", item_data)
        # Notify the mediator
        self.mediator.notify(self, "item_updated", item_data)

    # Delete an existing item
    def delete_item(self, item_id: int):
        # Logic to delete the item from the database
        print(f"Item with ID {item_id} Deleted")
        # Notify the mediator
        self.mediator.notify(self, "item_deleted", {"item_id": item_id})
