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
        self.datepickerPurchaseDate.date = None
        self.datepickerExpiryDate.date = None
        self.tbPrice.text = ""

    def btnConfirm_click(self, **event_args):
      purchase_date = self.datepickerPurchaseDate.date
      expiry_date = self.datepickerExpiryDate.date
      price = self.tbPrice.text
    
      # Validate inputs
      if not purchase_date:
          alert("Please select a purchase date.")
          return
      if expiry_date and purchase_date > expiry_date:
          alert("Purchase date cannot be after expiry date.")
          return
      if not price or not price.replace('.', '', 1).isdigit() or float(price) < 0:
          alert("Please enter a valid price (non-negative).")
          return
    
      price = float(price)
      
      anvil.server.call('check_off_item', self.item_id, purchase_date, expiry_date, price)
      alert("Item checked off successfully.")
      get_open_form().refresh_data_grid()


    def btnBack_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Command to close the form with this button
      self.raise_event("x-close-alert", value=42)
