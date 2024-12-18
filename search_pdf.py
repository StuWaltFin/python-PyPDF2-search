# import packages
import PyPDF2
import re
import os
import glob 
import sys

# Prints how far each query has searched in the pdf
def progress_bar(current, total, bar_length=40):
    progress = current / total
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block}{'-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()
    progress = current / total    
    if current == total: 
        print() # Ensure a newline at the end

# ------------------------- STEP ONE -------------------------
# OPTION I - get PDF filepath (option one) [NOT working]
def type_pdf_filepath():
    while True:
        pdf_path = input("Filepath of PDF to read (or 'back' to abort): ")
        # Check for existence
        if pdf_path.lower() == "back":
            print("Aborting to menu...\n\n")
            return None
        if not os.path.exists(pdf_path):
            print("Error: File not found. Please try again.\n")
            continue
        if not pdf_path.lower().endswith(".pdf"):
            print("Error: The file is not a PDF. Please provide a valid PDF file.\n")
            continue
        # Return pdf_path as string
        return pdf_path
    
# OPTION II - get PDF filepaths in directory [WORKING]
def get_pdfs_in_directory():
    pdf_list = glob.glob("pdfs/*.pdf")
    # check if there was anything returned at all
    if not pdf_list:
        print("No PDFs found in this directory (aborting to menu...)\n\n")
        return None

    # Prompt user to select a PDF
    while True:
            
        # loop to print found pdfs
        i = 0
        for pdf in pdf_list:
            i += 1
            print(f"{i}) {pdf}")

        print()
        usr_input = input("Which PDF would you like to search? (type a single number, or 'back'): ")
        # validate user input with try and except
        if usr_input.lower() == "back":
            print("Aborting to menu...\n\n")
            return None
        try:
            val = int(usr_input)
        except ValueError:
            print("\nERROR:  Invalid input, try again\n")
            continue

        if 0 < val <= len(pdf_list):
            pdf_path = pdf_list[val - 1]
            print(f"Selected {pdf_list[val - 1]}!\n")
        else:
            print("\nERROR: Input invalid, type number within range of list")
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
            while True:
                confirm = input("Confirm? [Y/n]: ").strip().lower()
                if confirm in ["y", ""]:
                    return search_terms 
                else:
                    print("Confirmation aborted.")
                    break       
            continue
        if usr_input not in search_terms:
                search_terms.append(usr_input)
        else:
            print(f"'{usr_input}' was already found in search terms.")

# OPTION II - use TXT document to get terms [UNTESTED]

# Helper function, parse txt contents and dispaly terms extracted
def get_txts_in_directory():
    print("NOTE: this program accepts .txt files of key terms, seperated by a comma")
    print("Example -> confidentiality, integrity, availibitliy (end of file)")
    print("If a read .txt file is not in this format, this step will abort to the user menu\n")
    
    txt_list = glob.glob("txt_terms/*.txt")
    
    # check if there was anything returned at all
    if not txt_list:
        print("No TXTs found in this directory (aborting to menu...)\n\n")
        return None
    
    while True:
        # loop to print found pdfs
        i = 0
        for txt in txt_list:
            i += 1
            print(f"{i}) {txt}")

        print("")
        usr_input = input("What TXT file would you like to use as search terms? (Type a single number): ")
        
        # validate user input with try and except
        try:
            val = int(usr_input)
        except ValueError:
            print("\nERROR: Invalid input, try again")
            continue 

        if 0 < val <= len(txt_list):
            txt_path = txt_list[val - 1]
            print(f"Selected {txt_list[val - 1]}!\n\n")
            
            # read text
            with open(txt_path, "r") as file:
                content = file.read()
                terms = [term.strip() for term in content.split(",")]

                # remove duplicates
                terms = list(set(terms))

                print("TESTING - parsed terms")
                print(terms)

            return terms
        else:
            print("\nInput invalid - type number within range of list")
            continue

# --------------------- SEARCH FUNCTION ---------------------
def search_pdf(reader, search_terms, num_pages):
    # dictionary to count total instances for each term (bc why not maybe you wanna know)
    term_pages = {term: [] for term in search_terms}
    term_counts = {term: 0 for term in search_terms}
    for term in search_terms:
        print(f"\nSearching for '{term}'...")
        term_found = False  # Boolean flag to check if we found the term
        
        for i in range(num_pages):
            # Extract text from page
            page = reader.pages[i]
            page_text = page.extract_text() or ""  # Default to empty string if text extraction fails (idk this seemed to work so we keep it)
            term_pages[term].append(i + 1) # Save the page number found to a dictionary to print it out at end

            # Search for the term using regex (case-insensitive)
            matches = list(re.finditer(rf'\b{term}\b', page_text, re.IGNORECASE))
            if matches:
                term_found = True
                term_counts[term] += len(matches)  # Increment by the number of matches foundh
                # Get a snippet around the match (50 characters before and after)
                # Get a snippet around the first match (50 characters before and after)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(page_text), match.end() + 50)
                    snippet = page_text[start:end].replace('\n', ' ')  # Replace newlines with spaces
                    
                    print(f"Found '{term}' on page {i + 1}:")
                    print(f"...{snippet}...")

            progress_bar(i + 1, num_pages)
        
        if not term_found:
            print(f"'{term}' not found in the document.")
    return term_counts, term_pages

# --------------------- USER MENU ---------------------
def user_menu():
    # STEP ONE - get pdf method, then path
    while True:
        print(" ------ Step one - type PDF filepath, or select filepath from list ------")
        print("1) View usable PDFs in this project directory")
        print("2) Type PDF filepath\n")
        usr_input_pdf = input("Select an option: ")
        if usr_input_pdf == "1":
            pdf_path = get_pdfs_in_directory()
        elif usr_input_pdf == "2":
            pdf_path = type_pdf_filepath()
        else:
            print("Invalid input - try again\n")
            continue

        # STEP TWO - get terms or txt path and parse
        while pdf_path: # boolean checks to see if step 1 was completed
            print("------ Step two - type terms, or select .TXT file containing terms ------")
            print("1) Type search terms in CLI")
            print("2) Use .txt file")

            usr_input_terms = input("Select an option: ")
            if usr_input_terms == "1":
                search_terms = type_terms()
                return pdf_path, search_terms
            elif usr_input_terms == "2":
                search_terms = get_txts_in_directory()
                return pdf_path, search_terms
            else:
                print("Invalid input - try again\n")
                continue
            

# --------------------- MAIN ---------------------
def main():
    pdf_path, search_terms = user_menu()
    reader = PyPDF2.PdfReader(pdf_path)
    # Get number of pages
    num_pages = len(reader.pages)
    # Call the function to search terms in the PDF
    term_counts, term_pages = search_pdf(reader, search_terms, num_pages)
    # Print summary of search
    print("\n ------------ Search summary ------------")

    for term, count in term_counts.items():
        if count == 0:
            print(f"No instances of '{term}' found in PDF")
        print(term)
        print(f"\tFound {count} times")
        pages = ', '.join(map(str, term_pages[term]))
        print(f"\tOn pages {pages}")

if __name__ == "__main__":
    main()
