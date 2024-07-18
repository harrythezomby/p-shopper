from ._anvil_designer import formGraphsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .formCatConsGraph import formCatConsGraph
from .formItemPriceHistGraph import formItemPriceHistGraph
from .formItemQuanConsGraph import formItemQuanConsGraph
from .formMonSpentHistGraph import formMonSpentHistGraph


class formGraphs(formGraphsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def tabClick(self, **event_args):
    """Tab funtionality adapted from Anvil forum user david.wylie's example. See https://anvil.works/forum/t/is-there-a-tab-bar-component/4291"""
    sender = event_args.get("sender", None)
    if not sender:
      print("Can't get sender  from : ", event_args)
      return

    for comp in self.flowTabs.get_components():
      if type(comp) is Button:
        if comp == sender:
          comp.background = "green"
          self.columnpanelContent.clear()
          self.columnpanelContent.add_component(comp.tag)
        else:
          comp.background = "#eee"

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.btnItemPriceHistTab.tag = formItemPriceHistGraph()
    self.btnCatConsTab.tag = formCatConsGraph()
    self.btnItemQuanConsTab.tag = formItemQuanConsGraph()
    self.btnMonSpentHistTab.tag = formMonSpentHistGraph()

    self.tabClick(sender = self.btnItemPriceHistTab)