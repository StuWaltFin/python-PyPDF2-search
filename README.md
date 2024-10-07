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
