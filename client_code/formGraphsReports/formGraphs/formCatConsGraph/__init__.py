from ._anvil_designer import formCatConsGraphTemplate
from anvil import *
import anvil.server
import plotly.graph_objs as go

class formCatConsGraph(formCatConsGraphTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'

        # Populate the category dropdown
        self.ddCatSelector.items = [(r['category_name'], r['category_id']) for r in anvil.server.call('get_all_categories_for_graphs')]

        # Set default selection
        self.ddCatSelector.selected_value = self.ddCatSelector.items[0][1]

        # Plot the initial graph
        self.plot_graph()

    def plot_graph(self):
        category_id = self.ddCatSelector.selected_value
        timeframe = self.timeframe
    
        data = anvil.server.call('get_category_consumption_data', category_id, timeframe)
        
        x = [item['date'] for item in data]
        y = [item['quantity'] for item in data]
    
        self.plotGraphCatCons.data = [go.Scatter(x=x, y=y, mode='lines+markers', name='Consumption')]
        self.plotGraphCatCons.layout.title = f"Category Consumption ({self.ddCatSelector.selected_value})"
        self.plotGraphCatCons.layout.xaxis.title = 'Date'
        self.plotGraphCatCons.layout.yaxis.title = 'Quantity'

    def ddCatSelector_change(self, **event_args):
        self.plot_graph()

    def btnWeek_click(self, **event_args):
        self.timeframe = 'week'
        self.plot_graph()

    def btnMonth_click(self, **event_args):
        self.timeframe = 'month'
        self.plot_graph()

    def btnYear_click(self, **event_args):
        self.timeframe = 'year'
        self.plot_graph()

