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
    
  def btnConfirm_click(self, **event_args):
      item_name = self.tbItemName.text
      quantity = self.tbQuantity.text
      category_id = self.ddCategory.selected_value
      brand = self.tbBrand.text
      store = self.tbStore.text
      aisle = self.tbAisle.text
      
      anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle)
      alert("Item added successfully.")
      self.raise_event("x-close-alert", value=42)


  def btnDiscard_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)