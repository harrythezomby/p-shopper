from ._anvil_designer import TestTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Test(TestTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Fetch items for a specific list and set them to the repeating panel
        # Replace 'your_list_id' with the actual list_id you want to test with
        self.refresh_items(1)  # Assuming '1' is the list_id for testing

    def refresh_items(self, list_id):
        items = anvil.server.call('get_all_items', int(list_id))
        self.repeating_panel_1.items = items
