# PDF Search Tool with PyPDF2 in Python

A command-line tool for searching terms in PDF documents. This tool allows users to input a PDF file path, enter search terms, and find occurrences of those terms along with snippets from the text.

## Features

- Validate PDF file paths before processing.
- Search for multiple terms in a PDF document.
- Display page numbers and snippets for each term found.
- Count total occurrences of each term in the document.

## Requirements

This project requires Python 3.6 or higher and the following packages:

- PyPDF2
- PyCryptodome (if you are working with encrypted PDFs)

You can install the required packages using the provided `requirements.txt` file.

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required packages:

```bash
pip install -r requirements.txt
```
## Usage
1. Run the script
```bash
python search_pdf.py
```
2. When prompted, give full filepath to PDF you want read
3. After os.path validation, enter terms you want to search for. Type "done" when you're finished entering, and you'll be prompted for confirmation (you can abort with any other input)
4. It will start to search (pretty slowly, dw its working), and found instances of each term will display their appropriate page number, and a snippet of its surrounding text

## Example
```bash
Filepath of PDF to read: /path/to/your/file.pdf
Type a term to search for: cybersecurity
Type a term to search for: threat
Type a term to search for: done
```


