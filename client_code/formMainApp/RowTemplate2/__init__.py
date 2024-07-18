from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..formCheckItem import formCheckItem

class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Populate category dropdown immediately
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

    def btnEdit_click(self, **event_args):
        # Populate category dropdown before showing the write view
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

        # Set the selected value to the current item's category
        current_category = self.item['category_id']
        if current_category:
            self.ddCategory.selected_value = current_category['category_id']
        
        self.dataRowPanelWriteView.visible = True
        self.dataRowPanelReadView.visible = False

    def btnSaveEdits_click(self, **event_args):
        self.dataRowPanelReadView.visible = True
        self.dataRowPanelWriteView.visible = False
        selected_category_id = self.ddCategory.selected_value
        category = anvil.server.call('get_category_by_id', selected_category_id)
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
        item_name = self.item['item_name']
        item_id = self.item['item_id']
        confirm_delete = confirm(f"Are you sure you want to delete the item '{item_name}'?")
        if confirm_delete:
            anvil.server.call('delete_item', item_id)
            alert(f"Item '{item_name}' deleted successfully.")
            self.raise_event('x-refresh-data')
            self.refresh_data_bindings()
            self.parent.parent.parent.refresh_data_grid()

    def btnCheck_click(self, **event_args):
        item_id = self.item['item_id']
        
        # Call the server function to get the list item row
        list_item_row = anvil.server.call('get_list_item_row', item_id)
        if list_item_row:
            list_item_id = list_item_row['list_item_id']
            content = formCheckItem(item_id=item_id, list_item_id=list_item_id, parent_form=self)
            alert(content=content, large=True, buttons=[], title="Check Off Item")
        else:
            alert("Error: List item not found.")
        self.refresh_data_bindings()
        self.parent.parent.parent.refresh_data_grid()