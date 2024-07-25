from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formInitiateShare import formInitiateShare
from .formSettings import formSettings
from .formCheckItem import formCheckItem
from .modTheming import modTheming
from .modInput import modInput
from .modPrepare import modPrepare
from .modInteraction import modInteraction

class formMainApp(formMainAppTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.prepare = modPrepare(self)  # Ensure this is defined before setting the event handler
        self.set_event_handler('x-refresh-data', self.prepare.refresh_data_grid)
        
        self.data = []
        self.headers = {
            'item_name': self.linkItemName,
            'quantity': self.linkQuantity,
            'category_id': self.linkCategory,
            'brand': self.linkBrand,
            'store': self.linkStore,
            'aisle': self.linkAisle
        }
        
        self.current_sort_column = 'item_name'
        self.current_sort_reverse = False

        # Initialize modules
        self.theming = modTheming(self)
        self.input = modInput(self)
        self.prepare = modPrepare(self)
        self.interaction = modInteraction(self)

        self.theming.apply_user_theme()  # Apply the user's theme on startup
      
        self.prepare.populate_lists_dropdown()
        self.prepare.update_expiry_warning()
        self.prepare.update_list_title()
        
        # Refresh data grid after initial population
        self.prepare.refresh_data_grid()

    def ddNewItemCategory_change(self, **event_args):
        self.input.ddNewItemCategory_change(**event_args)

    def btnCreateItem_click(self, **event_args):
        self.input.btnCreateItem_click(**event_args)

    def ddListSelector_change(self, **event_args):
        self.prepare.refresh_data_grid()
        self.prepare.update_list_title()

    def filter(self, **event_args):
        self.interaction.filter(**event_args)

    def search(self, **event_args):
        self.interaction.search(**event_args)

    def linkItemName_click(self, **event_args):
        self.interaction.sort_by_column('item_name')

    def linkQuantity_click(self, **event_args):
        self.interaction.sort_by_column('quantity')

    def linkCategory_click(self, **event_args):
        self.interaction.sort_by_column('category_id')

    def linkBrand_click(self, **event_args):
        self.interaction.sort_by_column('brand')

    def linkStore_click(self, **event_args):
        self.interaction.sort_by_column('store')

    def linkAisle_click(self, **event_args):
        self.interaction.sort_by_column('aisle')

    def btnShare_click(self, **event_args):
        alert(content=formInitiateShare(), large=False, buttons=[], title="Initiate Share")

    def btnReports_click(self, **event_args):
        open_form('formGraphsReports')

    def btnSettings_click(self, **event_args):
        alert(content=formSettings(), large=True, buttons=[], title="Settings")

    def btnRenameList_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        current_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
        content = TextBox(text=current_list_name)
        result = alert("Enter new name for the list:", buttons=[("OK", "ok")], content=content, title="Rename List")
        if result == "ok":
            new_name = content.text
            if new_name:
                anvil.server.call('rename_list', selected_list_id, new_name)
                self.prepare.populate_lists_dropdown()
                self.prepare.update_list_title()
  
    def btnNewList_click(self, **event_args):
        content = TextBox()
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        if result == "ok":
            new_name = content.text.strip().title()
            if new_name:
                user = anvil.users.get_user()
                anvil.server.call('create_new_list', new_name, user)
                self.prepare.populate_lists_dropdown()

    def btnExport_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
        download(csv_file)

    def check_off_item(self, item_id, list_id, **event_args):
        content = formCheckItem(item_id=item_id, list_id=list_id, parent_form=self)
        alert(content=content, large=True, buttons=[], title="Check Off Item")

    def btnLogout_click(self, **event_args):
        anvil.users.logout()
        open_form('formLogin')

    def btnDeleteList_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        if not selected_list_id:
            alert("No list selected to delete.")
            return
    
        selected_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
    
        confirm_delete = confirm(f"Are you sure you want to delete the list '{selected_list_name}'? This action cannot be undone.")
        if confirm_delete:
            anvil.server.call('delete_list', selected_list_id)
            alert(f"List '{selected_list_name}' and its items have been deleted successfully.")
            self.prepare.populate_lists_dropdown()
            self.prepare.update_list_title()
            self.prepare.refresh_data_grid()
