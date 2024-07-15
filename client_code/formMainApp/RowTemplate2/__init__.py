from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...State import categories as CATEGORIES


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.ddCategory.items = CATEGORIES

  def edit_item(self):
    # Convert the selected category name back to category_id
        selected_category_name = self.ddCategory.selected_value
        category = anvil.server.call('get_category_by_name', selected_category_name)
        anvil.server.call(
            'edit_item',
            item_id=self.item['item_id'],
            item_name=self.tbItemName.text,
            quantity=int(self.tbQuantity.text),
            category_id=category['category_id'],  # Convert category name back to category_id
            brand=self.tbBrand.text,
            store=self.tbStore.text,
            aisle=self.tbAisle.text)

  def btnEdit_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.dataRowPanelWriteView.visible = True
    self.dataRowPanelReadView.visible = False



  def btnSaveEdits_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.dataRowPanelReadView.visible = True
    self.dataRowPanelWriteView.visible = False
    
    self.edit_item()
    self.refresh_data_bindings()
    self.parent.parent.parent.refresh_data_grid()


