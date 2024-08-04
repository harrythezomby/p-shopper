from ._anvil_designer import formCheckItemTemplate
from anvil import *
import anvil.users
import anvil.server

class formCheckItem(formCheckItemTemplate):
    def __init__(self, list_item_id, **properties):
        self.init_components(**properties)
        
        # Store the list_item_id
        self.list_item_id = list_item_id

        # Fetch item details
        item_details = anvil.server.call('get_item_details', list_item_id)
        if item_details:
            self.lblItemInfo.text = f"Checking off: {item_details['item_name']} (Category: {item_details['category_name']}, Quantity: {item_details['quantity']})"
        else:
            alert("Item details could not be retrieved.")
            self.close()

    def btnConfirm_click(self, **event_args):
        purchase_date = self.datepickerPurchaseDate.date
        expiry_date = self.datepickerExpiryDate.date

        # Validation, assume 0 if no price is entered
        try:
            price = float(self.tbPrice.text)
        except ValueError:
            price = 0

        anvil.server.call('check_off_item', self.list_item_id, purchase_date, expiry_date, price)
        alert("Item checked off successfully.")
        self.raise_event('x-refresh-data')
        self.raise_event('x-close-alert', value=42)

    def btnBack_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Command to close the form with this button
        self.raise_event("x-close-alert", value=42)