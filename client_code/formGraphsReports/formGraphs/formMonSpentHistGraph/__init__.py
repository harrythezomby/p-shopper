from ._anvil_designer import formMonSpentHistGraphTemplate
from anvil import *
import plotly.graph_objects as go


class formMonSpentHistGraph(formMonSpentHistGraphTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
