from ._anvil_designer import formDeleteItemTemplate
from anvil import *


class formDeleteItem(formDeleteItemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btnBack_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)
