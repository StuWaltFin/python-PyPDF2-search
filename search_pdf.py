# import packages
import PyPDF2
import re
import os
import glob # wtf is glob lmao

# ------------------------- STEP ONE -------------------------
# OPTION I - get PDF filepath (option one) [UNTESTED]
def type_pdf_filepath():
    while True:
        pdf_path = input("Filepath of PDF to read (or 'back' to abort): ")
        # Check for existence
        if pdf_path.lower() == "back":
            print("Aborting to menu\n")
            return None
        if not os.path.exists(pdf_path):
            print("Error: File not found. Please try again.\n")
            continue
        if not pdf_path.lower().endswith(".pdf"):
            print("Error: The file is not a PDF. Please provide a valid PDF file.\n")
            continue
        # Return pdf_path as string
        return pdf_path
    
# OPTION II - get PDF filepaths in directory [UNTESTED]
def get_pdfs_in_directory():
    pdf_list = glob.glob("*.pdf")
    # check if there was anything returned at all
    if not pdf_list:
        print("No PDFs found in this directory (aborting to menu)\n")
        return None
    
    # loop to print found pdfs
    i = 0
    for pdf in pdf_list:
        i += 1
        print(f"{i}) {pdf}")

    # Prompt user to select a PDF
    while True:
        usr_input = input("So uhhhh, what'll it be chief? (type a single number): ")
        # validate user input with try and except
        try:
            val = int(usr_input)
        except ValueError:
            print("Invalid input, try again\n")
            continue

        if 0 < val <= len(pdf_list):
            pdf_path = pdf_list[val - 1]
            print(f"Selected {pdf_list[val - 1]}!\n")
        else:
            print("Input invalid - type number within range of list")
            continue
        return pdf_path

# ------------------------- STEP TWO -------------------------
# OPTION I - type terms in CLI [UNTESTED]
def type_terms():
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

    # Return search terms as a list
    return search_terms

# OPTION II - use TXT document to get terms [UNTESTED]
# FIXME parsing and input validation is going to be a hoot but we'll give it a shot
def get_txts_in_directory():
    txt_list = glob.glob("*.txt")
    # check if there was anything returned at all
    if not txt_list:
        print("No TXTs found in this directory (aborting to menu)\n")
        return None
    # loop to print found pdfs
    i = 0
    for txt in txt_list:
        i += 1
        print(f"{i}) - {txt}")
    while True:
        usr_input = input("So uhhhh, what'll it be chief?: ")
        # validate user input
        if 0 < usr_input <= len(txt_list):
            print(f"Selected {txt_list[usr_input]}!")
            txt_path = txt_path[usr_input]
        else:
            print("Input invalid - type number within range of list")
            continue
        return txt_path

# --------------------- SEARCH FUNCTION ---------------------
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
            match = re.search(rf'\b{term}\b', page_text, re.IGNORECASE)
            
            if match:
                term_found = True
                # Get a snippet around the match (50 characters before and after)
                start = max(0, match.start() - 50)
                end = min(len(page_text), match.end() + 50)
                snippet = page_text[start:end].replace('\n', ' ')  # Replace newlines with spaces
                
                print(f"Found '{term}' on page {i + 1}:")
                print(f"...{snippet}...")
        
        if not term_found:
            print(f"'{term}' not found in the document.")

# --------------------- USER MENU ---------------------
def user_menu():
    while True:
        print(" ------ Step one - type PDF filepath, or select filepath from list ------")
        print("1) Type PDF filepath")
        print("2) View usable PDFs in current directory\n")
        usr_input = input("Select an option: ")
        if usr_input == "1":
            pdf_path = type_pdf_filepath()
        if usr_input == "2":
            pdf_path = get_pdfs_in_directory()
        else:
            print("Invalid input - try again\n")
            continue
        while True:
            print("------ Step two - type terms, or select .TXT file containing terms ------")
            print("1) Type search terms in CLI")
            print("2) Use .txt file")
            if usr_input == "1":
                search_terms = type_terms()
            if usr_input == "2":
                search_terms = get_txts_in_directory()
            else:
                print("Invalid input - try again\n")
                continue
            return pdf_path, search_terms

# --------------------- MAIN ---------------------
def main():
    pdf_path, search_terms = user_menu()
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
    search_pdf(reader, search_terms, num_pages)

if __name__ == "__main__":
    main()
