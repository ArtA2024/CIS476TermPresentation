# mediators.py
from abc import ABC, abstractmethod

# Define the Mediator interface
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str, data: dict = None):
        pass


# Concrete implementation of the Mediator
class DashboardMediator(Mediator):
    def __init__(self):
        self.components = {}

    # Register a component with the mediator
    def register(self, component_name: str, component: object):
        self.components[component_name] = component

    # Notify the mediator about an event
    def notify(self, sender: object, event: str, data: dict = None):
        if event == "item_added":
            # Refresh the vault view when an item is added
            self.components["vault_view"].refresh(data)
        elif event == "item_deleted":
            # Refresh the vault view when an item is deleted
            self.components["vault_view"].refresh(data)
        elif event == "item_updated":
            # Refresh the vault view when an item is updated
            self.components["vault_view"].refresh(data)
