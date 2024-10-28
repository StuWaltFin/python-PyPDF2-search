# PDF Search Tool with PyPDF2 in Python

A command-line tool for searching terms in PDF documents. This tool allows users to input a PDF file path, enter search terms, and find occurrences of those terms along with snippets from the text.

## Features

- Add PDFs and TXT files to pre-made folders in the project, to search locally
- OR type in absolute paths of PDFs and TXT files
- Count total occurrences of each term found in a giben PDF
- See page numbers of each instance of page numbers

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
2. When prompted, either pick to search PDFs in the the local directory called "pdfs", or type in an absolute path
3. Same as step 2, provide TXT file or type in terms in the CLI
4. If you're typing terms in the CLI, type "done" when you're finished entering, and you'll be prompted for confirmation (you can abort with any other input)
5. It will start to search (see progress bar for completion percentage for each term), and found instances of each term will display their appropriate page numbers. 

## Example
```bash
Selected path/to/your/file.pdf!
Type a term to search for: (or 'done' to finish) cybersecurity
Type a term to search for: (or 'done' to finish) threat
Type a term to search for: (or 'done' to finish) threat
'threat' was already found in search terms.
Type a term to search for: (or 'done' to finish) done
Confirm? [Y/n]: y
Searching for 'threat'...
Progress: [########################################] 100.00%
```


