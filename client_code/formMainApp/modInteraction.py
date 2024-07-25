from anvil import *
import anvil.server
from .formCheckItem import formCheckItem

class modInteraction:
    def __init__(self, main_app):
        self.main_app = main_app

    def filter(self, **event_args):
        self.main_app.apply_filter_and_sort()

    def search(self, **event_args):
        self.main_app.apply_filter_and_sort(search_query=self.main_app.tbSearchList.text)

    def sort_by_column(self, column):
        if self.main_app.current_sort_column == column:
            self.main_app.current_sort_reverse = not self.main_app.current_sort_reverse
        else:
            self.main_app.current_sort_column = column
            self.main_app.current_sort_reverse = False

        self.main_app.apply_filter_and_sort()

    def sort_data(self, data):
        try:
            if self.main_app.current_sort_column == 'category_id':
                sorted_data = sorted(
                    data,
                    key=lambda x: x[self.main_app.current_sort_column]['category_name'].lower() if x[self.main_app.current_sort_column] else "",
                    reverse=self.main_app.current_sort_reverse
                )
            else:
                sorted_data = sorted(
                    data,
                    key=lambda x: str(x[self.main_app.current_sort_column]).lower() if x[self.main_app.current_sort_column] else "",
                    reverse=self.main_app.current_sort_reverse
                )
            return sorted_data
        except Exception as e:
            # Handle any exceptions that may occur during sorting
            print(f"Error during sorting: {e}")
            return data

    def apply_filter_and_sort(self, search_query=None):
        selected_category = self.main_app.ddCategorySelector.selected_value
        if selected_category:
            filtered_data = [item for item in self.main_app.data if item['category_id']['category_id'] == selected_category]
        else:
            filtered_data = self.main_app.data
    
        if search_query:
            filtered_data = [item for item in filtered_data if search_query.lower() in item['item_name'].lower()]
    
        sorted_data = self.sort_data(filtered_data)
        self.main_app.repeatListItems.items = sorted_data
    
        self.main_app.prepare.update_empty_label()  # Update the empty label after filtering and sorting
    
        for key, link in self.main_app.headers.items():
            if key == self.main_app.current_sort_column:
                link.icon = 'fa:caret-up' if self.main_app.current_sort_reverse else 'fa:caret-down'
            else:
                link.icon = None

    def create_new_list(self, **event_args):
        content = TextBox()
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        if result == "ok":
            new_name = content.text.strip().title()
            if new_name:
                user = anvil.users.get_user()
                anvil.server.call('create_new_list', new_name, user)
                self.main_app.prepare.populate_lists_dropdown()

    def export_list(self, **event_args):
        selected_list_id = self.main_app.ddListSelector.selected_value
        csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
        download(csv_file)

    def check_off_item(self, item_id, list_id, **event_args):
        content = formCheckItem(item_id=item_id, list_id=list_id, parent_form=self.main_app)
        alert(content=content, large=True, buttons=[], title="Check Off Item")

    def logout_user(self, **event_args):
        anvil.users.logout()
        open_form('formLogin')

    def delete_list(self, **event_args):
        selected_list_id = self.main_app.ddListSelector.selected_value
        if not selected_list_id:
            alert("No list selected to delete.")
            return
    
        selected_list_name = [item[0] for item in self.main_app.ddListSelector.items if item[1] == selected_list_id][0]
    
        confirm_delete = confirm(f"Are you sure you want to delete the list '{selected_list_name}'? This action cannot be undone.")
        if confirm_delete:
            anvil.server.call('delete_list', selected_list_id)
            alert(f"List '{selected_list_name}' and its items have been deleted successfully.")
            self.main_app.prepare.populate_lists_dropdown()
            self.main_app.prepare.update_list_title()
            self.main_app.prepare.refresh_data_grid()

