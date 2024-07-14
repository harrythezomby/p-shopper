from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formNewItem import formNewItem
from .formDeleteItem import formDeleteItem
from .formCheckItem import formCheckItem
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





  

  # When the new item button is clicked
  def btnNewItem_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formNewItem(),
    large=True,
    buttons = [],
    title="New Item")

    self.refresh_data_grid()

  def btnDeleteItem_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formDeleteItem(),
    large=False,
    buttons = [],
    title="Delete Item")

  def btnCheckItem_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formCheckItem(),
    large=True,
    buttons = [],
    title="Check Off Item")

  """def btnEditItem_click(self, **event_args):
    # Alert to display the form in a popup
    alert(content=formNewItem(), # For now, the edit button will just use the new item form for simplicity, this may be changed later on
    large=True,
    buttons = [],
    title="Edit Item")"""

 # def btnEditItem_click(self, **event_args):

    

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
    
