# Imports
from ._anvil_designer import formMonSpentHistGraphTemplate
from anvil import *
import anvil.users
import anvil.server
import plotly.graph_objs as go
import datetime

class formMonSpentHistGraph(formMonSpentHistGraphTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'
        self.radioWeek.selected = True

        # Plot the initial graph
        self.plot_graph()

    def plot_graph(self):
        timeframe = self.timeframe

        # Get data from the server
        data = anvil.server.call('get_money_spent_data', timeframe)
        
        # Sort data based on the actual date for correct chronological order
        data.sort(key=lambda x: x['date'])

        # Set headers of the graph
        x = [item['date'] for item in data]
        y = [item['amount_spent'] for item in data]

        # Timeframe settings
        if timeframe == 'week':
            x_labels = [f"Week {label}" for label in x]
            x_axis_title = 'Week'
        elif timeframe == 'month':
            x_labels = x  # Already formatted as month names
            x_axis_title = 'Month'
        elif timeframe == 'year':
            x_labels = [str(int(float(label))) for label in x]  # Ensure no decimal years
            x_axis_title = 'Year'

        # Bar graph settings
        self.plotMonSpentHist.data = [go.Bar(x=x_labels, y=y, name='Amount Spent')]
        self.plotMonSpentHist.layout = go.Layout(
            title="Money Spent History",
            xaxis=dict(title=x_axis_title, tickvals=x_labels, ticktext=x_labels),
            yaxis=dict(title='Amount Spent')
        )

        # Ensure the plot is refreshed
        self.plotMonSpentHist.redraw()

    # Timeframe selectors
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


