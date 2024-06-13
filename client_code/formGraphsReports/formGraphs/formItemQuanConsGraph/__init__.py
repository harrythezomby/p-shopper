from ._anvil_designer import formItemQuanConsGraphTemplate
from anvil import *
import plotly.graph_objects as go


class formItemQuanConsGraph(formItemQuanConsGraphTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
