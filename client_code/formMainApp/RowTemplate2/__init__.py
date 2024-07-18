from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..formCheckItem import formCheckItem

class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Bind the item details to the labels
        self.lblItemName.text = self.item['item_name']
        self.lblCategory.text = self.item['category_id']['category_name']
        self.lblQuantity.text = str(self.item['quantity'])
        self.lblBrand.text = self.item['brand']
        self.lblStore.text = self.item['store']
        self.lblAisle.text = self.item['aisle']

    def btnEdit_click(self, **event_args):
        self.dataRowPanelWriteView.visible = True
        self.dataRowPanelReadView.visible = False

        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]
        self.ddCategory.selected_value = self.item['category_id']['category_id']

    def btnSaveEdits_click(self, **event_args):
        selected_category_name = self.ddCategory.selected_value
        category = anvil.server.call('get_category_by_id', selected_category_name)
        anvil.server.call(
            'edit_item',
            item_id=self.item['item_id'],
            item_name=self.tbItemName.text,
            quantity=int(self.tbQuantity.text),
            category_id=category['category_id'],
            brand=self.tbBrand.text,
            store=self.tbStore.text,
            aisle=self.tbAisle.text
        )
        self.dataRowPanelReadView.visible = True
        self.dataRowPanelWriteView.visible = False
        self.refresh_data_bindings()
        self.raise_event('x-refresh-data')


