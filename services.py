import os
import PyPDF2
import pyperclip


def get_pdf_name():
    input_folder = "input"
    project_root = os.getcwd()  
    folder_path = os.path.join(project_root, input_folder)    
    
    filenames = os.listdir(folder_path) 
    return filenames[0]

def get_text_from_pdf(pdf_path, page_start=None, page_end=None):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        # Determine the page range
        if page_start is None:
            page_start = 0
        if page_end is None:
            page_end = len(reader.pages)
        
        for page_num in range(page_start, min(page_end, len(reader.pages))):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def process_text(text):
    # Replace newline characters with spaces
    text = text.replace("\n", " ").replace("- ", "")
    
    # Split text into substrings of max length with last character being a full stop
    max_length = 10000
    substrings = []
    while len(text) > max_length:
        substring_end = text.rfind(".", 0, max_length)
        if substring_end == -1:
            # If no full stop found in the first max_length characters,
            # just split at max_length
            substring_end = max_length
        substrings.append(text[:substring_end+1])
        text = text[substring_end+1:].strip()
    if text:  # Add the remaining text if any
        substrings.append(text)
    
    return substrings

def create_prompt(text_sample):
    chatgpt_prompt = f"""
    Make flashcards in tsv format with the given text.
    Use the format: question \\t answer \\t Ruby \\n 
    Make between 20 and 30 card that covers all the topics mentioned in the text

    \"\"\"
    {text_sample}
    \"\"\"
    """
    pyperclip.copy(chatgpt_prompt)
    print("Prompt copied to clipboard.")


if __name__ == "__main__":
    ind = 0
    page_start = 54
    page_end = 63

    raw_text = get_text_from_pdf( "input/" + get_pdf_name(), page_start, page_end)
    processed_text = process_text(raw_text)
    print(f"ind: {ind}, max ind: {len(processed_text)-1}")

    print(7)
    create_prompt(processed_text[ind])



