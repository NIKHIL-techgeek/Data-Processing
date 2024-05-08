import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class CSVMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Merger")
        self.files = []
        self.max_files = 12  # Maximum number of files
        
        # GUI setup
        self.label_text = tk.StringVar()
        self.label_text.set(f"Select CSV files (0/{self.max_files}):")
        tk.Label(root, textvariable=self.label_text, padx=20, pady=20).pack()
        
        self.add_file_button = tk.Button(root, text="Add CSV File", command=self.add_file, padx=20, pady=10)
        self.add_file_button.pack()
        self.merge_button = tk.Button(root, text="Merge and Save", command=self.merge_files, state='disabled', padx=20, pady=10)
        self.merge_button.pack()

    def update_label(self):
        # Update the label to show how many files have been added
        self.label_text.set(f"Select CSV files ({len(self.files)}/{self.max_files}):")
        if len(self.files) == self.max_files:
            self.merge_button.config(state='normal')
        elif len(self.files) > self.max_files:
            messagebox.showerror("Error", "Too many files selected. Only 12 files are allowed.")
            self.files.pop()  # Remove the extra file if added by mistake

    def add_file(self):
        # User selects a CSV file
        filename = filedialog.askopenfilename(title='Select a CSV File', filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if filename:
            # Process the file immediately to remove first three columns and store the dataframe
            df = pd.read_csv(filename)
            df = df.iloc[:, 3:]  # Skip the first three columns
            self.files.append(df)
            self.update_label()

    def merge_files(self):
        # Merge all dataframes
        if len(self.files) == self.max_files:
            concatenated_df = pd.concat(self.files, ignore_index=True)
            output_filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if output_filename:
                concatenated_df.to_csv(output_filename, index=False)
                messagebox.showinfo("Success", "The files have been successfully merged and saved.")
                self.files = []  # Reset the file list
                self.update_label()  # Reset the label
                self.merge_button.config(state='disabled')
        else:
            messagebox.showerror("Error", "Insufficient files. Please add exactly 12 files.")

def main():
    root = tk.Tk()
    app = CSVMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
