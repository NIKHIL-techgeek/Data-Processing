import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os

def process_report(report_type):
    # Open file dialog to select the report CSV file
    filepath = filedialog.askopenfilename(title=f"Select {report_type.capitalize()} Report CSV",
                                          filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        messagebox.showerror("Error", "No file was selected. Please select a file.")
        return
    
    try:
        # Load the report based on type and apply transformations
        report = pd.read_csv(filepath)
        if 'sip:Anonymous@Anonymous.invalid' in report.to_string():
            report = report[~report.applymap(lambda x: 'sip:Anonymous@Anonymous.invalid' in str(x)).any(axis=1)]

        # Common transformation for Users column
        if 'Users' in report.columns:
            report['Users'] = report['Users'].str.split(';').str[-1].str.strip()

        # Specific transformations for each report type
        if report_type == 'call':
            report['ANI'] = report['ANI'].str.replace('tel:\+1', '', regex=True)
            final_columns = ['ANI', 'Date', 'Duration', 'Total Queue', 'Users', 'Queue', 'Wrap-up', 'Conversation ID']
        elif report_type == 'email':
            final_columns = ['From', 'Remote', 'To', 'Subject', 'Date', 'Duration', 'Total Queue', 'Users', 'Wrap-up', 'Conversation ID']
        elif report_type == 'live_chat':
            final_columns = ['Remote', 'Date', 'Duration', 'Total Queue', 'Users', 'Queue', 'Wrap-up', 'Conversation ID']

        final_report = report[final_columns]

        # Save the transformed report
        base, _ = os.path.splitext(filepath)
        output_filepath = f"{base}_transformed_{report_type}.csv"
        final_report.to_csv(output_filepath, index=False)

        messagebox.showinfo("Success", f"The {report_type} report has been processed and saved:\n{output_filepath}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI window
root = tk.Tk()
root.title("Report Transformer")

# Buttons for each report type
tk.Button(root, text="Process Call Report", command=lambda: process_report('call')).pack(fill=tk.X, padx=50, pady=5)
tk.Button(root, text="Process Email Report", command=lambda: process_report('email')).pack(fill=tk.X, padx=50, pady=5)
tk.Button(root, text="Process Live Chat Report", command=lambda: process_report('live_chat')).pack(fill=tk.X, padx=50, pady=5)

# Run the GUI loop
root.mainloop()