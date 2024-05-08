import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def process_ivr_report():
    filepath = filedialog.askopenfilename(title="Select IVR Report CSV", filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        messagebox.showerror("Error", "No file was selected. Please select a file.")
        return

    try:
        # Load the report
        report = pd.read_csv(filepath)

        # Retain only specified columns
        report = report[['Campaign ID', 'Campaign Name', 'Dials']]

        # Calculate the sum of 'Dials'
        if 'Dials' in report.columns:
            sum_dials = report['Dials'].sum()

            # Prepare a summary DataFrame
            summary_df = pd.DataFrame([{"Campaign ID": "", "Campaign Name": "Summary", "Dials": sum_dials}])

            # Concatenate the original report with the summary DataFrame
            report = pd.concat([report, pd.DataFrame([{}]), summary_df], ignore_index=True)

        # Save the transformed report
        base, _ = os.path.splitext(filepath)
        output_filepath = f"{base}_transformed.csv"
        report.to_csv(output_filepath, index=False)

        messagebox.showinfo("Success", f"The IVR report has been processed and saved:\n{output_filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI window
root = tk.Tk()
root.title("IVR Report Processor")

# Button for processing the IVR report
tk.Button(root, text="Process IVR Report", command=process_ivr_report).pack(fill=tk.X, padx=50, pady=5)

# Run the GUI loop
root.mainloop()
