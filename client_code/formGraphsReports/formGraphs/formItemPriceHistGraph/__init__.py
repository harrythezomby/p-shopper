from ._anvil_designer import formItemPriceHistGraphTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import plotly.graph_objects as go


class formItemPriceHistGraph(formItemPriceHistGraphTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
