from ._anvil_designer import formMainAppTemplate
from anvil import *
from .formNewItem import formNewItem


class formMainApp(formMainAppTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btnNewItem_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(content=formNewItem(),
    title="New Item")