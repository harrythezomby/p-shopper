from ._anvil_designer import formWeeklySpendReportTemplate
from anvil import *
import anvil.server

class formWeeklySpendReport(formWeeklySpendReportTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Generate the initial report
        self.generate_report()

    def generate_report(self):
        # Fetch report data from the server
        spending_changes = anvil.server.call('get_weekly_spending_report')

        # Create report in markdown format
        report_markdown = """
### Weekly Spending Comparison Report

| Week | Date Range | Total Spending | Change | % Change |
| --- | --- | --- | --- | --- |
"""
        for week, total, change, percent_change, week_range in spending_changes:
            report_markdown += f"| {week} | {week_range[0]} to {week_range[1]} | ${total:.2f} | {'+' if change > 0 else ''}{change:.2f} | {'+' if percent_change > 0 else ''}{percent_change:.2f}% |\n"

        # Display the report in the rich text component
        self.textReport.content = report_markdown

    def btnExport_click(self, **event_args):
        # Generate report markdown
        report_markdown = self.textReport.content

        # Create a BlobMedia object for the markdown file
        media = anvil.BlobMedia("text/markdown", report_markdown.encode(), name="weekly_spending_report.md")

        # Download the file
        download(media)