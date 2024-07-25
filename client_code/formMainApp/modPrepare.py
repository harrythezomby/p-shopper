import anvil.server
import anvil.users

class modPrepare:
    def __init__(self, main_app):
        self.main_app = main_app

    def populate_lists_dropdown(self):
        user = anvil.users.get_user()
        lists = anvil.server.call('get_all_lists', user)
        self.main_app.ddListSelector.items = [(l['list_name'], l['list_id']) for l in lists if l['list_name']]
        if lists:
            self.main_app.ddListSelector.selected_value = lists[0]['list_id']
            self.refresh_data_grid()  # Corrected this line
        else:
            self.main_app.ddListSelector.selected_value = None
            self.main_app.data = []
            self.main_app.apply_filter_and_sort()
            self.main_app.lblIsEmpty.text = "The currently selected list is empty."
            self.main_app.lblIsEmpty.visible = True

    def refresh_data_grid(self, **event_args):
        selected_list_id = self.main_app.ddListSelector.selected_value
        if selected_list_id:
            self.main_app.data = anvil.server.call('get_all_items', selected_list_id)
            self.main_app.apply_filter_and_sort(search_query=self.main_app.tbSearchList.text)
            self.populate_category_dropdown()
            self.update_empty_label()
        else:
            self.main_app.data = []
            self.main_app.apply_filter_and_sort()
            self.populate_category_dropdown()
            self.update_empty_label()

    def populate_category_dropdown(self):
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.main_app.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "New Category"), ("Remove Category", "Remove Category")]
        selected_list_id = self.main_app.ddListSelector.selected_value
        if selected_list_id:
            categories = anvil.server.call('get_categories_for_list', selected_list_id)
            self.main_app.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]

    def update_empty_label(self):
        if not self.main_app.data:
            self.main_app.lblIsEmpty.text = "The currently selected list is empty."
            self.main_app.lblIsEmpty.visible = True
        else:
            self.main_app.lblIsEmpty.visible = False


    def update_list_title(self):
        selected_list_id = self.main_app.ddListSelector.selected_value
        if selected_list_id:
            list_name = [item[0] for item in self.main_app.ddListSelector.items if item[1] == selected_list_id][0]
            self.main_app.lblListTitle.text = list_name

