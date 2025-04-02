# PDF Compressor GUI

A simple graphical user interface (GUI) application built with Python and Tkinter to compress PDF files using the Apryse PDFNet SDK (formerly PDFTron). It offers different compression levels to help reduce PDF file sizes.

## Features
* Easy-to-use graphical interface.
* Select input PDF file via a standard file dialog.
* Select output directory via a standard directory dialog.
* Specify a custom output filename (a default based on the input name is suggested).
* Choose between:
    * **Normal Compress:** Uses standard PDFNet optimization settings.
    * **Super Compress:** Uses more aggressive image compression settings (lower quality, smaller size).
* Displays original and compressed file sizes (in MB).
* Calculates and displays the percentage reduction in file size.
* Prompts for confirmation before overwriting existing files.
* Basic error handling for file operations and PDF processing issues.
* Powered by the PDFNetPython3 SDK.

## Requirements

* **Python 3.x**
* **Tkinter:** Usually included with standard Python installations on Windows and macOS. On Linux, you might need to install it separately (e.g., `sudo apt-get install python3-tk`).
* **Apryse PDFNetPython3 SDK:**
    * This is a **commercial library**. You need to download it from the [Apryse website](https://www.apryse.com/develop/python/).
    * A license key (obtained from Apryse) might be required for full functionality or to remove trial limitations. The script can run in trial mode without a key initially.

## Installation

1.  **Clone or Download:** Get the script file (e.g., `pdf_compressor_gui.py`).
2.  **Install Python & Tkinter:** Ensure you have Python 3 installed and Tkinter is available for your OS.
3.  **Install PDFNetPython3 SDK:**
    * Download the appropriate SDK package for your operating system (Windows/macOS/Linux) from the [Apryse Python SDK page](https://www.apryse.com/develop/python/).
    * Follow the installation instructions provided by Apryse. This usually involves extracting the package and ensuring the `PDFNetPython3` module is accessible to your Python environment
    * *Note: Installation might differ from a standard `pip install`. Refer to the official Apryse documentation.*

## Usage

1.  **Run the script** from your terminal:
    ```bash
    python pdf_compressor_gui.py
    ```
2.  The application window will appear.
3.  **Select Input File:** Click the "Select..." button next to "PDF File:" and choose the PDF you want to compress.
4.  **Select Output Directory:** Click the "Select..." button next to "Save in:" and choose the folder where the compressed file should be saved.
5.  **Set Output Name:** An output filename (e.g., `yourfile_opt.pdf`) will be suggested. You can edit this name in the "New File Name:" field if desired.
6.  **Choose Compression Type:** Select either 'Normal Compress' or 'Super Compress' from the dropdown menu.
7.  **Compress:** Click the "Compress PDF" button. The button text will change to "Compressing..." while processing.
8.  **Wait:** The time taken depends on the PDF size and complexity, and the chosen compression level.
9.  **Result:**
    * On success, a message box will appear showing the original size, the new size, and the percentage reduction.
    * If an error occurs (e.g., file not found, permission denied, PDFNet error), an error message box will be displayed.
    * If the output file already exists, you will be asked to confirm overwriting it.
