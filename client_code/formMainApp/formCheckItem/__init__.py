from ._anvil_designer import formCheckItemTemplate
from anvil import *
import anvil.server

class formCheckItem(formCheckItemTemplate):
  def __init__(self, item_id, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      
      self.item_id = item_id
      self.load_item_details()

  def load_item_details(self):
      item = anvil.server.call('get_item_details', self.item_id)
      self.lblItemInfo.text = f"Checking off: {item['item_name']}"
      self.purchase_date = self.datepickerPurchaseDate.date
      self.expiry_date = self.datepickerExpiryDate.date
      self.price = self.tbPrice.text

  def btnConfirm_click(self, **event_args):
      purchase_date = self.datepickerPurchaseDate.date
      expiry_date = self.datepickerExpiryDate.date
      price = float(self.tbPrice.text)
      
      anvil.server.call('check_off_item', self.item_id, purchase_date, expiry_date, price)
      alert("Item checked off successfully.")
      get_open_form().refresh_data_grid()
      self.parent.raise_event('x-close-alert')


  def btnBack_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)
