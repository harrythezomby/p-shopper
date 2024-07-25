from ._anvil_designer import formReportsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .formItemCompReport import formItemCompReport
from .formItemExpReport import formItemExpReport
from .formWeeklySpendReport import formWeeklySpendReport

class formReports(formReportsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Initialize report forms
    self.item_comp_report_form = formItemCompReport()
    self.item_exp_report_form = formItemExpReport()
    self.weekly_spend_report_form = formWeeklySpendReport()

    # Store the initialized forms in the button tags
    self.btnItemCompTab.tag = self.item_comp_report_form
    self.btnItemExpiryTab.tag = self.item_exp_report_form
    self.btnWeeklySpendCompTab.tag = self.weekly_spend_report_form

  def tabClick(self, **event_args):
    """Tab functionality adapted from Anvil forum user david.wylie's example. See https://anvil.works/forum/t/is-there-a-tab-bar-component/4291"""
    sender = event_args.get("sender", None)
    if not sender:
      print("Can't get sender from:", event_args)
      return

    for comp in self.flowTabs.get_components():
      if isinstance(comp, Button):
        if comp == sender:
          comp.background = "green"
          self.columnpanelContent.clear()
          try:
            self.columnpanelContent.add_component(comp.tag)
          except TypeError as e:
            print(f"Error adding component: {e}")
        else:
          comp.background = "#eee"

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.tabClick(sender=self.btnItemCompTab)
