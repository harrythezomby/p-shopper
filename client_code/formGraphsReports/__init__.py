from ._anvil_designer import formGraphsReportsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .formGraphs import formGraphs
from .formReports import formReports


class formGraphsReports(formGraphsReportsTemplate):
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
    self.btnGraphsTab.tag = formGraphs()
    self.btnReportsTab.tag = formReports()

    self.tabClick(sender = self.btnGraphsTab)

  def btnBack_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('formMainApp')





