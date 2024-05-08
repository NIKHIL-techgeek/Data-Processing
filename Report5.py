import tkinter as tk
from PIL import Image , ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import PyPDF2
root=tk.Tk()

canvas=tk.Canvas(root,width=600,height=300)
canvas.grid(columnspan=3, rowspan=3)

# logo
logo = Image.open("C:\gui\pdf extracter\logo.png")
logo=ImageTk.PhotoImage(logo)
logo_label=tk.Label(image=logo)
# cannot skip this line
logo_label.image=logo

# placing logo inside windows object
logo_label.grid(column=1,row=0)

# instructions
instructions= tk.Label(root,text="Select a PDF file on your computer to extract all text",font="Raleway")
instructions.grid(columnspan=3,column=0,row=1)

# function 
def open_file():
    browse_text.set("loading...")
    file = filedialog.askopenfile(parent=root, mode="rb", title="Choose a file", filetype=[("Pdf File", "*.pdf")])

    if file:
            # Use PdfFileReader instead of PdfReader
            read_pdf = PyPDF2.PdfReader(file)
            
            # Use reader.pages[page_number] instead of reader.getPage(page_number)
            page_number = 0  # Change the page number as needed
            page = read_pdf.pages[page_number]
            
            # Extract text from the page
            page_content = page.extract_text()
            
            print(page_content)
            # text_box
            text_box=tk.Text(root,height=10,width=45,padx=15,pady=15)
            text_box.insert(1.0,page_content)
            text_box.tag_configure("center",justify="center")
            text_box.tag_add("center",1.0,"end")
            text_box.grid(column=1,row=3)
            
            browse_text.set("Browse")
            
            
            

# browse button 
browse_text=tk.StringVar()
browse_btn=tk.Button(root,textvariable=browse_text,command=lambda:open_file(),font="Raleway",bg="#20bebe",fg="white",height=2,width=15)
browse_text.set("Browse")
browse_btn.grid(column=1,row=2)

canvas=tk.Canvas(root,width=600,height=250)
canvas.grid(columnspan=3)
root.mainloop()

