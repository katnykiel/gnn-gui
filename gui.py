import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

# from reportlab.pdfgen import canvas
import csv
from models import get_matgl_formation_energy

from inputs import get_structure_from_file, get_structure_from_MatProj
from inputs import make_structure_image
import os
from PIL import Image, ImageTk

text_visualization = None  # Define text_visualization as a global variable
structure = None
ase_atoms = None
# entry_url = None
# entry_api = None

def predict_properties():
    global text_visualization  # Access the global variable
    if text_visualization is not None:
        # Get test structure from file
        # structure = get_structure_from_file("example_files/NaCl.cif")
        # structure object is now create when load button is pressed
        try:
            # Predict properties
            final_structure, final_energy, eform = get_matgl_formation_energy(structure)
            # Update the "Visualization Area" with the results
            text_visualization.delete(1.0, tk.END)  # Clear the previous content
            text_visualization.insert(
                tk.END,
                f"The final relaxed structure is:\n{final_structure}\n\nThe final energy is {float(final_energy):.3f} eV.\n\nThe predicted formation energy for this structure is {float(eform.numpy()):.3f} eV/atom.",
            )
        except Exception as e:
            text_visualization.delete(1.0, tk.END) 
            text_visualization.insert(tk.END, f"Error predicting properties: {e}")


def export_to_pdf():
    result = text_visualization.get(1.0, tk.END)
    c = canvas.Canvas("prediction_result.pdf")
    width, height = c._pagesize
    c.drawString(100, height - 100, "Prediction Result:")
    c.drawString(100, height - 130, result)
    c.showPage()
    c.save()


def export_to_csv():
    result = text_visualization.get(1.0, tk.END)
    with open("prediction_result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Prediction Result"])
        writer.writerow([result])


def open_documentation():
    # Implement the logic to open the documentation in a web browser or file viewer.
    pass  # Add your code here


def change_text_color():
    color = askcolor()[1]  # Open a color picker and get the selected color
    text_visualization.config(foreground=color)


def change_background_color():
    color = askcolor()[1]  # Open a color picker and get the selected color
    text_visualization.config(bg=color)


def change_font():
    font = Font(
        family="Helvetica",
        size=12,
        weight="normal",
        slant="roman",
        underline=0,
        overstrike=0,
    )
    font = askopenfilename(
        filetypes=[("Font Files", "*.ttf")]
    )  # Open a file dialog to select a font file
    text_visualization.config(font=font)

def load_structure(entry_url, entry_api):
    global structure
    global ase_atoms
    
    try:
        url = entry_url.get()
        api_key = entry_api.get()
        mp_id = url.split('/')[-1]    
        structure, ase_atoms = get_structure_from_MatProj(api_key, mp_id)
        text_visualization.delete(1.0, tk.END) 
        text_visualization.insert(tk.END, "Loaded Structure from Materials Project.")
        return structure, ase_atoms
    except Exception as e:
        text_visualization.delete(1.0, tk.END) 
        text_visualization.insert(tk.END, 
                                  f"API key and/or URL entered incorrectly: {e}")
        return None
    
def visualize_structure():
    global image_placeholder
    make_structure_image(ase_atoms, img="mp_load.png")
    image = Image.open('mp_load.png')
    desired_size = (250, 250)
    image = image.resize(desired_size, Image.ANTIALIAS)
    
    tk_structure_image = ImageTk.PhotoImage(image)
    image_placeholder.config(image=tk_structure_image)
    image_placeholder.image = tk_structure_image
    # structure_image = tk.Label(frame, image=tk_structure_image)
    # structure_image.image = tk_structure_image
    # structure_image.pack(side=tk.TOP, padx=10)  # Adjust positioning

def test_GUI():
    root = tk.Tk()
    root.title("GNN Model Selector")

    global text_visualization  # Access the global variable
    global image_placeholder
    
    # Create a frame to hold the entire content
    frame = tk.Frame(root)
    frame.grid(padx=10, pady=10)

    # Create a style for custom theming
    style = ttk.Style()
    style.configure(
        "TButton", padding=5, relief="flat", background="#008CBA", foreground="white"
    )
    style.map("TButton", background=[("active", "#005A8C")])

    # Input for Crystal Structure Data URL
    label_url = tk.Label(frame, text=("Enter Crystal Structure Data URL:\n"
                                      'https://materialsproject.org/materials/mp-22851\n'
                                      'or\n'
                                      'mp-22851'))
    label_url.grid(row=0, column=0, columnspan=2, pady=5)
    entry_url = tk.Entry(frame, width=50)
    entry_url.grid(row=1, column=0, columnspan=2, pady=5)

    # Input box for API KEY 
    label_api = tk.Label(frame, text="Enter Materials Project API key:")
    label_api.grid(row=2, column=0, columnspan=2, pady=5)
    entry_api = tk.Entry(frame, width=50)
    entry_api.grid(row=3, column=0, columnspan=2, pady=5)
    
    # Load Structure Button
    load_structure_properties = tk.Button(
        frame, text="Load Structure",     
        command=lambda: load_structure(entry_url, entry_api)
    )
    load_structure_properties.grid(row=4, column=0, pady=5)
    
    # Image Placeholder
    image_placeholder = tk.Label(frame)
    image_placeholder.config(width=50, height=25, bg='gray')  
    image_placeholder.grid(row=1, column=3, columnspan=3,rowspan=10, pady=10)
    
    #Visualize Structure Button
    visualize_structure_properties = tk.Button(
        frame, text="Visualize Structure",
        command=visualize_structure
    )
    visualize_structure_properties.grid(row=4, column=1, pady=5)
    
    # Dropdown for Materials Project Data
    label_materials = tk.Label(frame, text="Materials Project Data:")
    label_materials.grid(row=5, column=0, pady=5)
    materials_var = tk.StringVar()
    materials_dropdown = ttk.Combobox(
        frame, textvariable=materials_var, values=["Data1", "Data2", "Data3"]
    )
    materials_dropdown.grid(row=6, column=0, columnspan=2, pady=5)

    # Dropdown for GNN Models
    label_gnn = tk.Label(frame, text="Select Graph Neural Network Model:")
    label_gnn.grid(row=7, column=0, pady=5)
    gnn_var = tk.StringVar()
    gnn_dropdown = ttk.Combobox(
        frame,
        textvariable=gnn_var,
        values=["GNN Model 1", "GNN Model 2", "GNN Model 3"],
    )
    gnn_dropdown.grid(row=8, column=0, columnspan=2, pady=5)

    # Visualization Area with Scrollbar
    label_visualization = tk.Label(frame, text="Visualization of the Process:")
    label_visualization.grid(row=9, column=0, pady=5)
    text_visualization = tk.Text(frame, height=10, width=50)
    text_visualization.grid(row=10, column=0, columnspan=2)
    scrollbar = tk.Scrollbar(frame, command=text_visualization.yview)
    scrollbar.grid(row=10, column=2, sticky='ns')
    text_visualization.config(yscrollcommand=scrollbar.set)

    # Customization Buttons
    btn_change_text_color = tk.Button(
        frame, text="Change Text Color", command=change_text_color
    )
    btn_change_text_color.grid(row=11, column=0, pady=5)

    btn_change_background_color = tk.Button(
        frame, text="Change Background Color", command=change_background_color
    )
    btn_change_background_color.grid(row=11, column=1, pady=5)

    btn_change_font = tk.Button(frame, text="Change Font", command=change_font)
    btn_change_font.grid(row=12, column=0, columnspan=2, pady=5)

    # Export Buttons
    btn_export_pdf = tk.Button(frame, text="Export to PDF", command=export_to_pdf)
    btn_export_pdf.grid(row=13, column=0, pady=5)

    btn_export_csv = tk.Button(frame, text="Export to CSV", command=export_to_csv)
    btn_export_csv.grid(row=13, column=1, pady=5)

    # Documentation Button
    btn_documentation = tk.Button(
        frame, text="Documentation and Help Center", command=open_documentation
    )
    btn_documentation.grid(row=14, column=0, columnspan=2, pady=5)

    # Prediction Button
    btn_predict_properties = tk.Button(
        frame, text="Predict Properties", command=predict_properties
    )
    btn_predict_properties.grid(row=15, column=0, columnspan=2, pady=5)

    root.mainloop()
