# import packages
import PyPDF2
import re
import os
import sys

# Prints how far each query has searched in the pdf
def progress_bar(current, total, bar_length=40):
    progress = current / total
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block}{'-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()

# Get a valid PDF file path
def get_valid_pdf_path():
    while True:
        pdf_path = input("Filepath of PDF to read: ")
        # Check for existence
        if not os.path.exists(pdf_path):
            print("Error: File not found. Please try again.\n")
            continue
        if not pdf_path.lower().endswith(".pdf"):
            print("Error: The file is not a PDF. Please provide a valid PDF file.\n")
            continue
        # Passes validation
        return pdf_path

# Function to search for terms in the PDF
def search_pdf(reader, search_terms, num_pages):
    # dictionary to count total instances for each term (bc why not maybe you wanna know)
    term_counts = {term: 0 for term in search_terms}
    for term in search_terms:
        print(f"\nSearching for '{term}'...")
        term_found = False  # Boolean flag to check if we found the term
        
        for i in range(num_pages):
            # Extract text from page
            page = reader.pages[i]
            page_text = page.extract_text() or ""  # Default to empty string if text extraction fails (idk this seemed to work so we keep it)
            
            # Search for the term using regex (case-insensitive)
            matches = re.findall(rf'\b{term}\b', page_text, re.IGNORECASE)
            if matches:
                term_found = True
                term_counts[term] += len(matches)  # Increment by the number of matches foundh
                # Get a snippet around the match (50 characters before and after)
                # Get a snippet around the first match (50 characters before and after)
                first_match = re.search(rf'\b{term}\b', page_text, re.IGNORECASE)
                if first_match:
                    start = max(0, first_match.start() - 50)
                    end = min(len(page_text), first_match.end() + 50)
                    snippet = page_text[start:end].replace('\n', ' ')  # Replace newlines with spaces
                    
                    print(f"Found '{term}' on page {i + 1}:")
                    print(f"...{snippet}...")
        
        if not term_found:
            print(f"'{term}' not found in the document.")
    return term_counts 

def main():
    pdf_path = get_valid_pdf_path()
    reader = PyPDF2.PdfReader(pdf_path)

    # Get number of pages
    num_pages = len(reader.pages)

    # Search for strings
    search_terms = []
    while True:
        usr_input = input("Type a term to search for: (or 'done' to finish) ")
        usr_input = usr_input.lower()  # Make it lowercase for uniformity
        if usr_input == "done":
            confirm = input("Confirm? [Y/n]: ").strip().lower()
            if confirm in ["y", ""]:
                break 
            else:
                print("Confirmation aborted.")
                continue       
        if usr_input not in search_terms:
            search_terms.append(usr_input)
        else:
            print(f"'{usr_input}' was already found in search terms.")

    # Call the function to search terms in the PDF
    term_counts = search_pdf(reader, search_terms, num_pages)

    # Print summary of search
    print("\n Search summary:")
    for term, count in term_counts.items():
        if count == 0:
            print(f"'No instances of {term} found in PDF")
        print(f"'{term}' found {count} times")


if __name__ == "__main__":
    main()
