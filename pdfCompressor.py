"""
Created on Sun Mar  7 
Refactored on Tue Apr  1

@author: Lucas 
"""
import tkinter as tk
from tkinter import ttk  # Use ttk for more modern widgets
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import os

# Import PDFNetPython3 - Make sure it is installed and licensed
try:
    from PDFNetPython3 import PDFNet, PDFDoc, Optimizer, SDFDoc, ImageSettings, OptimizerSettings
except ImportError:
    messagebox.showerror("Import Error",
                         "PDFNetPython3 library not found. "
                         "Please ensure it is installed correctly.")
    exit() # Exit if the main library cannot be imported

# --- Constants ---
BG_COLOR = '#0497e5'
DEFAULT_SUFFIX = "_opt"
MB_DIVISOR = 1024 * 1024 # To convert bytes to megabytes

class PdfCompressorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Compressor - PUC Minas Poços de Caldas")
        self.master.geometry('600x350') # Window dimensions
        self.master.config(bg=BG_COLOR)
        self.master.resizable(False, False) # Prevent resizing

        # Application state variables
        self.input_pdf_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.original_file_size = None

        # PDFNet Initialization (IMPORTANT!)
        # Replace "YOUR_PDFNET_LICENSE_KEY" with your key or remove if using the trial version
        try:
             # PDFNet.Initialize("YOUR_PDFNET_LICENSE_KEY") # Uncomment and add your key here
             PDFNet.Initialize() # For trial version or key set via environment variable
        except Exception as e:
             messagebox.showerror("PDFNet Error", f"Failed to initialize PDFNet: {e}")
             self.master.quit() # Close the application if initialization fails

        self._create_widgets()

    def _create_widgets(self):
        # --- Main frame for better organization ---
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        # Configure columns to center content (optional)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.columnconfigure(2, weight=1)


        # --- Input File Widgets ---
        lbl_input = ttk.Label(main_frame, text="PDF File:")
        lbl_input.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)

        self.entry_input = ttk.Entry(main_frame, textvariable=self.input_pdf_path, width=40, state='readonly')
        self.entry_input.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)

        btn_select_input = ttk.Button(main_frame, text="Select...", command=self._select_input_file)
        btn_select_input.grid(row=0, column=2, padx=5, pady=10)

        # --- Output Directory Widgets ---
        lbl_output_dir = ttk.Label(main_frame, text="Save in:")
        lbl_output_dir.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)

        self.entry_output_dir = ttk.Entry(main_frame, textvariable=self.output_dir_path, width=40, state='readonly')
        self.entry_output_dir.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        btn_select_output_dir = ttk.Button(main_frame, text="Select...", command=self._select_output_dir)
        btn_select_output_dir.grid(row=1, column=2, padx=5, pady=10)

        # --- New File Name Widgets ---
        lbl_output_name = ttk.Label(main_frame, text="New File Name:")
        lbl_output_name.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)

        self.entry_output_name = ttk.Entry(main_frame, textvariable=self.output_filename, width=40)
        self.entry_output_name.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)
        ttk.Label(main_frame, text=".pdf").grid(row=2, column=2, padx=0, pady=10, sticky=tk.W) # Add extension visually


        # --- Compression Type Widgets ---
        lbl_compress_type = ttk.Label(main_frame, text="Compression Type:")
        lbl_compress_type.grid(row=3, column=0, padx=5, pady=10, sticky=tk.W)

        self.combo_compress_type = ttk.Combobox(main_frame, values=('Normal Compress', 'Super Compress'), state='readonly', width=38)
        self.combo_compress_type.grid(row=3, column=1, padx=5, pady=10, sticky=tk.EW)
        self.combo_compress_type.current(0) # Set 'Normal Compress' as default

        # --- Convert Button ---
        self.btn_convert = ttk.Button(main_frame, text="Compress PDF", command=self._compress_pdf, style='Accent.TButton')
        # The 'Accent.TButton' style might not work on all themes/OSs, it's an example.
        self.btn_convert.grid(row=4, column=0, columnspan=3, pady=20)

        # Style configuration (optional, to highlight the button)
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Calibri', 12, 'bold'))


    def _select_input_file(self):
        filename = askopenfilename(
            title="Select PDF File",
            filetypes=[('PDF Files', '*.pdf')]
        )
        if not filename: # If the user cancels
            return

        try:
            self.original_file_size = os.path.getsize(filename)
            self.input_pdf_path.set(filename)

            # Suggest output name automatically
            base_name = os.path.basename(filename)
            name_without_ext, _ = os.path.splitext(base_name)
            self.output_filename.set(f"{name_without_ext}{DEFAULT_SUFFIX}")

            # If the output directory hasn't been set yet, suggest the same as the input directory
            if not self.output_dir_path.get():
                 self.output_dir_path.set(os.path.dirname(filename))

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filename}")
            self.input_pdf_path.set("")
            self.output_filename.set("")
            self.original_file_size = None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while selecting the file: {e}")
            self.input_pdf_path.set("")
            self.output_filename.set("")
            self.original_file_size = None

    def _select_output_dir(self):
        directory = askdirectory(title="Select the folder to save the compressed file")
        if directory:
            self.output_dir_path.set(directory)

    def _validate_inputs(self):
        """Checks if all required fields are filled."""
        if not self.input_pdf_path.get():
            messagebox.showwarning('Warning', 'Select the PDF file to compress.')
            return False
        if not self.output_dir_path.get():
            messagebox.showwarning('Warning', 'Select the folder where the file will be saved.')
            return False
        if not self.output_filename.get():
            messagebox.showwarning('Warning', 'Set the name for the new file.')
            return False
        if not self.combo_compress_type.get():
            # This shouldn't happen with state='readonly' and a default value, but it's good to check
            messagebox.showwarning('Warning', 'Select the compression type.')
            return False
        return True

    def _compress_pdf(self):
        if not self._validate_inputs():
            return

        input_path = self.input_pdf_path.get()
        output_dir = self.output_dir_path.get()
        output_name = self.output_filename.get()
        compress_type = self.combo_compress_type.get()

        # Ensure the filename has the .pdf extension
        if not output_name.lower().endswith(".pdf"):
            output_name += ".pdf"

        output_path = os.path.join(output_dir, output_name)

        # Check if the output file already exists
        if os.path.exists(output_path):
             if not messagebox.askyesno("File Exists",
                                       f"The file '{output_name}' already exists in this folder.\n"
                                       "Do you want to overwrite it?"):
                 return # Cancel the operation if the user doesn't want to overwrite


        # --- Disable the button during processing ---
        self.btn_convert.config(state=tk.DISABLED, text="Compressing...")
        self.master.update_idletasks() # Force GUI update

        doc = None # Initialize doc outside try to ensure finally can access it
        try:
            doc = PDFDoc(input_path)
            doc.InitSecurityHandler() # Necessary if the PDF is password-protected

            if compress_type == "Normal Compress":
                Optimizer.Optimize(doc)
            elif compress_type == "Super Compress":
                image_settings = ImageSettings()
                # Aggressive settings for maximum compression (may lose quality)
                image_settings.SetCompressionMode(ImageSettings.e_jpeg)
                image_settings.SetQuality(1) # Very low JPEG quality (1-100)
                image_settings.SetImageDPI(96, 72) # Low DPI (suitable for screen, bad for printing)
                # Force recompression even if the image is already compressed
                image_settings.ForceRecompression(True)
                # Force applying settings even if it increases size (rarely useful)
                # image_settings.ForceChanges(True)

                opt_settings = OptimizerSettings()
                opt_settings.SetColorImageSettings(image_settings)
                opt_settings.SetGrayscaleImageSettings(image_settings)
                # Other optimization options can be added here
                # opt_settings.RemoveMetadata()
                # opt_settings.RemoveEmbeddedFonts() # Warning: might break PDF rendering

                Optimizer.Optimize(doc, opt_settings)
            else:
                 # Unexpected case, although the combobox is readonly
                 raise ValueError(f"Unknown compression type: {compress_type}")


            # Save the optimized document
            # SDFDoc.e_linearized optimizes for fast web view
            doc.Save(output_path, SDFDoc.e_linearized)

            # Calculate sizes and show result
            new_file_size = os.path.getsize(output_path)
            original_mb = self.original_file_size / MB_DIVISOR
            new_mb = new_file_size / MB_DIVISOR
            reduction_percent = (1 - (new_file_size / self.original_file_size)) * 100 if self.original_file_size > 0 else 0

            messagebox.showinfo(
                'Compression Complete',
                f"File compressed successfully!\n"
                f"----------------------------\n"
                f"Original File : {original_mb:.2f} MB\n"
                f"Optimized File: {new_mb:.2f} MB\n"
                f"Reduction: {reduction_percent:.1f}%"
            )

        except PDFNet.Error as e:
             messagebox.showerror("PDFNet Error", f"An error occurred during compression:\n{e}")
        except FileNotFoundError:
             messagebox.showerror("Error", f"Input file not found: {input_path}")
             self.input_pdf_path.set("") # Clear the field if the file no longer exists
        except PermissionError:
             messagebox.showerror("Permission Error",
                                f"Permission denied to read the input file or "
                                f"save in '{output_dir}'. Check permissions.")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        finally:
            # --- Ensure the PDF document is closed ---
            if doc:
                try:
                    doc.Close()
                except Exception as e:
                    print(f"Warning: Error closing PDF document: {e}") # Log for debugging

            # --- Re-enable the button ---
            self.btn_convert.config(state=tk.NORMAL, text="Compress PDF")


if __name__ == "__main__":
    # Check if the library can be initialized before creating the window
    try:
        # Try to initialize temporarily to check license/installation
        # PDFNet.Initialize("YOUR_PDFNET_LICENSE_KEY") # Or use keyless initialization for trial
        PDFNet.Initialize()
        PDFNet.Terminate() # Terminate the temporary initialization
    except Exception as e:
        messagebox.showerror("Critical PDFNet Error",
                             f"Could not initialize the PDFNet library.\n"
                             f"Check your installation and license.\nError: {e}")
        exit()

    root = tk.Tk()
    app = PdfCompressorApp(root)
    root.mainloop()
