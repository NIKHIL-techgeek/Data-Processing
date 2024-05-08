# Entegrus Auto-Report
# Developed by: Ben Renaud & Vivian Tang
# Created: 4/11/2023
# Last update: 01-19-2024

# Need to import tkinter and pandas library to use file explorer windows and utilize data manipulation
import sys
import pandas as pd
import tkinter as Tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re

# This dictionary is used to assign the "Unique ID" to each User's interaction.
# When new CSR's are hired we need to update this portion of the code.
user_dict = {
    'Abbey Haynes': '5556',
    'Amy Adams': '4295',
    'Andrea Dowding': '4822',
    'Andrea Spurrell': '4297',
    'Barb McAllister': '4565',
    'Beth Blair': '4556',
    'Crystal Byrne': '4247',
    'Eleni Sofocleous': '4244',
    'Erin Edwards': '4566',
    'Jacqui Wright': '4826',
    'Janina Zylstra': '5332',
    'Joel Tulloch': '4292',
    'Kim Birkby': '4282',
    'Laura Cyples': '5557',
    'Lisa Mallory': '4250',
    'Lori Evely': '5336',
    'Melissa Hurteau': '4831',
    'Melissa Shackleton': '5335',
    'Michelle Gillies': '5331',
    'Stacey Blokzyl': '4551',
    'Sue Konc': '4564',
    'Sharie Morrison': '5226',
    'Kim Heyninck': '5587',
    'Misty Harris': '5598',
    'Megan Young': '5597',
    'Kristyn Clayton': '5596',
    'Heather Vaughan': '5620',
    "Colleen O\'Rourke": '5621'
}


# This function is used to prompt the user when the Survey report is generate successfully
def show_popup(message=""):
    root = Tk()
    root.withdraw()  # hide the root window
    messagebox.showinfo("Concentrix Survey Script",
                        "Concentrix Survey Report generation completed successfully!\n\nYou will need to encrypt the .txt file then send it over FTP.\n\nHave a great day!")
    root.destroy()  # destroy the root window


# This function is used to prompt the user to pick a location to save the generated Survey report
def get_export_dir():
    root = Tk()
    root.withdraw()  # hide the root window
    export_dir = filedialog.asksaveasfilename(defaultextension='.csv',
                                              initialfile='CSR_Entegrus_YYYYMMDD',
                                              title='Select the Concentrix Report folder to save the new Survey Reports in')
    return export_dir  # return the file location for the Survey Report

# create the Tkinter root window and hide it
root = Tk()
root.withdraw()

try:
    # This is for the File explorer window that pops up for choosing the proper file.
    filepath = filedialog.askopenfilename(title="Find and Open the Sample_Survey_File.csv you Downloaded to Continue",
                                          filetypes=(("csv", "*.csv"),  # only allow .csv files
                                                     ("all files", "*.*")))
    if not filepath:
        messagebox.showerror("Error", "No file was selected. Please try again and choose a file.")
        sys.exit(1)

    file = open(filepath, 'r')
    data = pd.read_csv(file)  # read data from file

    # delete Name column (Full Export Completed, Partial Result Timestamp, Filters)
    data.drop('Full Export Completed', inplace=True, axis=1)
    data.drop('Partial Result Timestamp', inplace=True, axis=1)
    data.drop('Filters', inplace=True, axis=1)
    print("\nDeleted the first three columns\n", data)

    # delete row if it starts with 'sip:' in the ANI column
    data = data[~data.ANI.str.contains('sip')]
    print("\nDeleted rows that contain \'sip\'\n", data)

    # delete 'tel:+1' (first 6 characters)
    data['ANI'] = data['ANI'].str[6:]
    print("\nDeleted the \'tel:+1\' in the ANI column\n", data)

    # delete duplicate ANI rows (phone numbers), keep the last instance
    data = data.drop_duplicates(subset=["ANI"], keep='last')
    print("\nDeleted the duplicate rows in the ANI column, keeping the last instance\n", data)

    # delete names after the first semicolon
    data["Users"] = data["Users"].str.split(';').str[0]
    print("\nDeleted names after the first semicolon\n", data)

    # sort Time column ascending (ANI)
    data = data.sort_values('ANI', ascending=True)
    print("\nSorted the ANI column in ascending order\n", data)

    # use map function to apply the dictionary to the 'User' column and fill in the 'Unique ID' column
    data['Unique ID'] = data['Users'].map(user_dict)
    print("\nAssigned Unique ID to each user interaction\n", data)

    export_path_csv = get_export_dir()

    if not export_path_csv:
        messagebox.showerror("Error", "No export directory selected.")
        sys.exit(1)

    # Convert dates from MM/DD/YYYY HH:MM format
    for idx, date in enumerate(data['Date']):
        if re.match(r'\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2}', date):
            print("Date format is correct:", date)
        else:
            print("Date format is incorrect. Please ensure dates are in MM/DD/YYYY HH:MM format.")
            messagebox.showerror("Error",
                                 "Date format in the file is incorrect. Please ensure dates are in MM/DD/YYYY HH:MM format.\n\nTry to open the Sample Survey File.csv and save it, then try this again.")
            sys.exit(1)

    # Convert 'Date' column to datetime object
    data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y %H:%M')

    # Convert 'Date' column to string with desired format
    data['Date'] = data['Date'].dt.strftime('%m/%d/%Y %I:%M %p')

# This try/except block will catch any errors
# that happen while generating the survey file
except Exception as e:
    messagebox.showerror("Error",
                         str("No report was generated.\n\nPlease contact IT if there is a problem or raise a ticket "
                             "using helpdesk@entegrus.com."))
    sys.exit(1)

# This try/except block will catch any errors
# that occur during the saving of the generated file
try:
    data.to_csv(export_path_csv, index=False)
    print("CSV Report exported to:", export_path_csv)

    export_path_txt = export_path_csv.replace('.csv', '.txt')
    data.to_csv(export_path_txt, sep='\t', index=False,
                date_format='%m/%d/%Y %I:%M %p')  # Specify the date format for the text file

except FileNotFoundError:
    messagebox.showerror("Error", "File not found.")
    sys.exit(1)

except Exception as e:
    messagebox.showerror("Error", "An unexpected error occurred: {}".format(str(e)))
    sys.exit(1)

except Exception as e:
    messagebox.showerror("Error",
                         str("No report was exported.\n\nPlease contact IT if there is a problem or raise a ticket "
                             "using helpdesk@entegrus.com."))
    sys.exit(1)

# show pop-up message if the program executed successfully
show_popup()

file.close()
sys.exit(0)