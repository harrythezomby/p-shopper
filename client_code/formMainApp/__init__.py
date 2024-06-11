from ._anvil_designer import formMainAppTemplate
from anvil import *
from .formNewItem import formNewItem
from .formDeleteItem import formDeleteItem
from .formCheckItem import formCheckItem
from .formInitiateShare import formInitiateShare


class formMainApp(formMainAppTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # When the new item button is clicked
  def btnNewItem_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formNewItem(),
    large=True,
    buttons = [],
    title="New Item")

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

  def btnEditItem_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Alert to display the form in a popup
    alert(content=formNewItem(), # For now, the edit button will just use the new item form for simplicity, this may be changed later on
    large=True,
    buttons = [],
    title="Edit Item")

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
    
