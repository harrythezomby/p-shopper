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

    def populate_category_dropdown(self):
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

    def btnEdit_click(self, **event_args):
        self.dataRowPanelWriteView.visible = True
        self.dataRowPanelReadView.visible = False
        self.populate_category_dropdown()
        selected_category = self.item['category_id']
        if selected_category:
            self.ddCategory.selected_value = selected_category['category_id']
        else:
            self.ddCategory.selected_value = None

    def btnSaveEdits_click(self, **event_args):
        self.dataRowPanelReadView.visible = True
        self.dataRowPanelWriteView.visible = False
        selected_category_id = self.ddCategory.selected_value
        anvil.server.call(
            'edit_item',
            item_id=self.item['item_id'],
            item_name=self.tbItemName.text,
            quantity=int(self.tbQuantity.text),
            category_id=selected_category_id,
            brand=self.tbBrand.text,
            store=self.tbStore.text,
            aisle=self.tbAisle.text
        )
        self.refresh_data_bindings()
        self.parent.parent.parent.refresh_data_grid()

