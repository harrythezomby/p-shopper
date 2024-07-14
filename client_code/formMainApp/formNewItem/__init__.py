from ._anvil_designer import formNewItemTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class formNewItem(formNewItemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  # Populate the category dropdown
    categories = anvil.server.call('get_all_categories')
    self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

  def btnDiscard_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)

  def btnConfirm_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_name = self.tbItemName.text
    quantity = int(self.tbQuantity.text)
    category_id = self.ddCategory.selected_value
    brand = self.tbBrand.text
    store = self.tbStore.text
    aisle = self.tbAisle.text
    
    # Add the item to the database via server call
    anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle)
    
    # Clear the form fields
    self.tbItemName.text = ''
    self.tbQuantity.text = ''
    self.ddCategory.selected_value = None
    self.tbBrand.text = ''
    self.tbStore.text = ''
    self.tbAisle.text = ''
