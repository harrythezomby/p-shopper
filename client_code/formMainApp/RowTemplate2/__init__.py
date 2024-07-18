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
        self.set_data_bindings()

    def set_data_bindings(self):
        self.lblItemName.text = self.item['item_name']
        self.lblQuantity.text = str(self.item['quantity'])
        self.lblCategory.text = self.item['category_id']['category_name'] if self.item['category_id'] else "None"
        self.lblBrand.text = self.item['brand']
        self.lblStore.text = self.item['store']
        self.lblAisle.text = self.item['aisle']

    def btnEdit_click(self, **event_args):
        self.dataRowPanelWriteView.visible = True
        self.dataRowPanelReadView.visible = False

    def btnSaveEdits_click(self, **event_args):
        self.dataRowPanelReadView.visible = True
        self.dataRowPanelWriteView.visible = False
        selected_category_name = self.ddCategory.selected_value
        category = anvil.server.call('get_category_by_name', selected_category_name)
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
        self.refresh_data_bindings()
        self.parent.parent.parent.refresh_data_grid()

    def btnDelete_click(self, **event_args):
        list_item_id = self.item['list_item_id']
        confirm_delete = confirm("Are you sure you want to delete this item?")
        if confirm_delete:
            anvil.server.call('delete_item', list_item_id)
            alert("Item deleted successfully.")
            self.raise_event('x-refresh-data')

    def btnCheck_click(self, **event_args):
        list_item_id = self.item['list_item_id']
        content = formCheckItem(list_item_id, parent_form=self)
        alert(content=content, large=True, buttons=[], title="Check Off Item")
