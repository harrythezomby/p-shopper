from ._anvil_designer import RowTemplate3Template
from anvil import *

class RowTemplate3(RowTemplate3Template):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Bind the item details to the labels
        self.lblItemName.text = self.item['item_name']
        self.lblCategory.text = self.item['category_id']['category_name']
        self.lblQuantity.text = str(self.item['quantity'])
        self.lblBrand.text = self.item['brand']
        self.lblStore.text = self.item['store']
        self.lblAisle.text = self.item['aisle']
