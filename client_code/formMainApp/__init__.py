from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formInitiateShare import formInitiateShare
from .formSettings import formSettings


class formMainApp(formMainAppTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens
    self.refresh_data_grid()

    # Populate the category dropdown
    categories = anvil.server.call('get_all_categories')
    self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
    self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories]
    
    # Perform initial filter to show all items
    self.filter()

  def filter(self, **event_args):
      selected_category = self.ddCategorySelector.selected_value
      print(f"Selected category: {selected_category}")  # Debug statement
      self.repeatListItems.items = anvil.server.call('filter_items', selected_category)


  def search(self, **event_args):
    self.repeatListItems.items = anvil.server.call(
    'search_items',
    self.tbSearchList.text)

  def refresh_data_grid(self, **event_args):
      self.repeatListItems.items = anvil.server.call('get_all_items')


  def btnCreateItem_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_name = self.tbNewItemName.text
    category_id = self.ddNewItemCategory.selected_value

    # If quantity is blank, assume 1
    if self.tbNewItemQuantity.text == 0 or None:
      quantity = 1
    else:
      quantity = self.tbNewItemQuantity.text

    none = "None" # Assuming blank/N/A value, can be changed to whatever here easily

    # If brand is empty assume no brand
    if self.tbNewItemBrand.text == "" or None:
      brand = none
    else:
      brand = self.tbNewItemBrand.text

    # If store is empty assume no store
    if self.tbNewItemStore.text == "" or None:
      store = none
    else:
      store = self.tbNewItemStore.text
      
    # If aisle is empty assume no aisle
    if self.tbNewItemAisle.text == "" or None:
      aisle = none
    else:
      aisle = self.tbNewItemAisle.text
    
    anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle)
    alert("Item added successfully.")
    self.refresh_data_grid()









# Other functions
  def btnShare_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formInitiateShare(), # For now, the edit button will just use the new item form for simplicity, this may be changed later on
    large=False,
    buttons = [],
    title="Initiate Share")

  def btnReports_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('formGraphsReports')

  def btnSettings_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(content=formSettings(), # For now, the edit button will just use the new item form for simplicity, this may be changed later on
    large=False,
    buttons = [],
    title="Settings")


    

    
