import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from reportlab.pdfgen import canvas
import csv

text_visualization = None  # Define text_visualization as a global variable

from pymatgen.core import Lattice, Structure
import matgl # library for stuff
from matgl.ext.ase import Relaxer


def predict_properties():
    global text_visualization  # Access the global variable
    if text_visualization is not None:
        # Load GNN model
        pot = matgl.load_model("M3GNet-MP-2021.2.8-PES")

        # Load input structure
        struct = Structure.from_file("NaCL.cif")

        # Relax structure with MatGL
        relaxer = Relaxer(potential=pot)
        relax_results = relaxer.relax(struct, fmax=0.01, verbose=True)

        # Extract results
        final_structure = relax_results["final_structure"]
        final_energy = relax_results["trajectory"].energies[-1]

        # Predict formation energy with MEGNet
        model = matgl.load_model("MEGNet-MP-2018.6.1-Eform")
        eform = model.predict_structure(final_structure)

        # Update the "Visualization Area" with the results
        text_visualization.delete(1.0, tk.END)  # Clear the previous content
        text_visualization.insert(
            tk.END,
            f"The final relaxed structure is:\n{final_structure}\n\nThe final energy is {float(final_energy):.3f} eV.\n\nThe predicted formation energy for this structure is {float(eform.numpy()):.3f} eV/atom.",
        )


# def predict_properties():
#     global text_visualization  # Access the global variable
#     if text_visualization is not None:
#         # Implement your prediction logic here
#         # Update the "Visualization Area" with the results
#         result = "Sample prediction result"
#         text_visualization.delete(1.0, tk.END)  # Clear the previous content
#         text_visualization.insert(tk.END, result)


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


def main():
    root = tk.Tk()
    root.title("GNN Model Selector")

    global text_visualization  # Access the global variable

    # Create a frame to hold the entire content
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Create a style for custom theming
    style = ttk.Style()
    style.configure(
        "TButton", padding=5, relief="flat", background="#008CBA", foreground="white"
    )
    style.map("TButton", background=[("active", "#005A8C")])

    # Input for Crystal Structure Data URL
    label_url = tk.Label(frame, text="Enter Crystal Structure Data URL:")
    label_url.pack(pady=10)
    entry_url = tk.Entry(frame, width=50)
    entry_url.pack(pady=10)

    # Dropdown for Materials Project Data
    label_materials = tk.Label(frame, text="Materials Project Data:")
    label_materials.pack(pady=10)
    materials_var = tk.StringVar()
    materials_dropdown = ttk.Combobox(
        frame, textvariable=materials_var, values=["Data1", "Data2", "Data3"]
    )
    materials_dropdown.pack(pady=10)

    # Dropdown for GNN Models
    label_gnn = tk.Label(frame, text="Select Graph Neural Network Model:")
    label_gnn.pack(pady=10)
    gnn_var = tk.StringVar()
    gnn_dropdown = ttk.Combobox(
        frame,
        textvariable=gnn_var,
        values=["GNN Model 1", "GNN Model 2", "GNN Model 3"],
    )
    gnn_dropdown.pack(pady=10)

    # Visualization Area with Scrollbar
    label_visualization = tk.Label(frame, text="Visualization of the Process:")
    label_visualization.pack(pady=10)
    text_visualization = tk.Text(frame, height=10, width=50)
    text_visualization.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(frame, command=text_visualization.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_visualization.config(yscrollcommand=scrollbar.set)

    # Customization Buttons
    btn_change_text_color = tk.Button(
        frame, text="Change Text Color", command=change_text_color
    )
    btn_change_text_color.pack(side=tk.TOP, padx=10)  # Adjust positioning

    btn_change_background_color = tk.Button(
        frame, text="Change Background Color", command=change_background_color
    )
    btn_change_background_color.pack(side=tk.TOP, padx=10)  # Adjust positioning

    btn_change_font = tk.Button(frame, text="Change Font", command=change_font)
    btn_change_font.pack(side=tk.TOP, padx=10)  # Adjust positioning

    # Export Buttons
    btn_export_pdf = tk.Button(frame, text="Export to PDF", command=export_to_pdf)
    btn_export_pdf.pack(side=tk.TOP, padx=10)  # Adjust positioning

    btn_export_csv = tk.Button(frame, text="Export to CSV", command=export_to_csv)
    btn_export_csv.pack(side=tk.TOP, padx=10)  # Adjust positioning

    # Documentation Button
    btn_documentation = tk.Button(
        frame, text="Documentation and Help Center", command=open_documentation
    )
    btn_documentation.pack(side=tk.TOP, padx=10)  # Adjust positioning

    # Prediction Button
    btn_predict_properties = tk.Button(
        frame, text="Predict Properties", command=predict_properties
    )
    btn_predict_properties.pack(side=tk.TOP, padx=10)  # Adjust positioning

    root.mainloop()


if __name__ == "__main__":
    main()
