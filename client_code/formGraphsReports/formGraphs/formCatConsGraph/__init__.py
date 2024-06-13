from ._anvil_designer import formCatConsGraphTemplate
from anvil import *
import plotly.graph_objects as go


class formCatConsGraph(formCatConsGraphTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
