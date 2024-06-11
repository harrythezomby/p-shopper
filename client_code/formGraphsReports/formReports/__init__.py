from ._anvil_designer import formReportsTemplate
from anvil import *


class formReports(formReportsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
