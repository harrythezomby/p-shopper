from ._anvil_designer import formItemPriceHistGraphTemplate
from anvil import *
import anvil.server
import plotly.graph_objs as go
import datetime

class formItemPriceHistGraph(formItemPriceHistGraphTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'
        self.radioWeek.selected = True

        # Populate the item dropdown
        self.ddItemSelector.items = [(r['item_name'], r['item_name']) for r in anvil.server.call('get_all_items_for_graphs')]

        # Set default selection
        self.ddItemSelector.selected_value = self.ddItemSelector.items[0][1]

        # Plot the initial graph
        self.plot_graph()

    def plot_graph(self):
        item_name = self.ddItemSelector.selected_value
        timeframe = self.timeframe

        data = anvil.server.call('get_item_price_history_data', item_name, timeframe)
        
        # Sort data based on the actual date for correct chronological order
        data.sort(key=lambda x: x['date'])

        x = [item['date'] for item in data]
        y = [item['price'] for item in data]

        if timeframe == 'week':
            x_labels = [f"Week {label}" for label in x]
            x_axis_title = 'Week'
        elif timeframe == 'month':
            x_labels = x  # Already formatted as month names
            x_axis_title = 'Month'
        elif timeframe == 'year':
            x_labels = [str(int(float(label))) for label in x]  # Ensure no decimal years
            x_axis_title = 'Year'

        # Find the item name
        item_name = self.ddItemSelector.selected_value

        self.plotItemPriceHist.data = [go.Scatter(x=x_labels, y=y, mode='lines+markers', name='Price')]
        self.plotItemPriceHist.layout = go.Layout(
            title=f"{item_name} Price History",
            xaxis=dict(title=x_axis_title, tickvals=x_labels, ticktext=x_labels),
            yaxis=dict(title='Price')
        )

        # Ensure the plot is refreshed
        self.plotItemPriceHist.redraw()

    def ddItemSelector_change(self, **event_args):
        self.plot_graph()

    def radioWeek_change(self, **event_args):
        if self.radioWeek.selected:
            self.timeframe = 'week'
            self.plot_graph()

    def radioMonth_change(self, **event_args):
        if self.radioMonth.selected:
            self.timeframe = 'month'
            self.plot_graph()

    def radioYear_change(self, **event_args):
        if self.radioYear.selected:
            self.timeframe = 'year'
            self.plot_graph()