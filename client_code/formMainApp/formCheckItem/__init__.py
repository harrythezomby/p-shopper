from ._anvil_designer import formCheckItemTemplate
from anvil import *
import anvil.server

class formCheckItem(formCheckItemTemplate):
    def __init__(self, list_item_id, parent_form, **properties):
        self.init_components(**properties)
        
        # Store the list_item_id and parent form
        self.list_item_id = list_item_id
        self.parent_form = parent_form

        # Fetch item details
        item_details = anvil.server.call('get_item_details', list_item_id)
        self.lblItemInfo.text = f"Checking off: {item_details['item_name']} (Category: {item_details['category_name']}, Quantity: {item_details['quantity']})"

    def btnConfirm_click(self, **event_args):
        purchase_date = self.datepickerPurchaseDate.date
        expiry_date = self.datepickerExpiryDate.date
        price = float(self.tbPrice.text)

        anvil.server.call('check_off_item', self.list_item_id, purchase_date, expiry_date, price)
        alert("Item checked off successfully.")
        self.parent_form.refresh_data_grid()
        self.raise_event('x-close-alert', value=42)

    def btnBack_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Command to close the form with this button
        self.raise_event("x-close-alert", value=42)