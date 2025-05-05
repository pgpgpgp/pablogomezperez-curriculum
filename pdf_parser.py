import sys
import os
import subprocess

# Fix for linting errors - we'll handle the import differently
# First check if PyPDF2 is installed
try:
    import PyPDF2  # type: ignore
except ImportError:
    print("PyPDF2 not found. Installing...")
    try:
        # More reliable than os.system
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        import PyPDF2  # type: ignore
    except (subprocess.CalledProcessError, ImportError):
        print("Failed to install PyPDF2. Please install it manually with:")
        print("    pip install PyPDF2")
        sys.exit(1)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            # Using PyPDF2.PdfReader even if linter doesn't recognize it
            reader = PyPDF2.PdfReader(file)  # type: ignore
            text = ""
            for page_num in range(len(reader.pages)):
                try:
                    page_text = reader.pages[page_num].extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                    else:
                        print(f"Warning: Could not extract text from page {page_num+1}. It may be an image or have no text content.")
                except Exception as e:
                    print(f"Warning: Error extracting text from page {page_num+1}: {str(e)}")
            return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py <path_to_pdf>")
        sys.exit(1)

    # Normalize the path for the operating system
    pdf_path = os.path.normpath(os.path.abspath(sys.argv[1]))
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)

    print(f"Processing PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    if not text.strip():
        print("Warning: No text was extracted from the PDF. It may be an image-only PDF or protected.")
        sys.exit(1)
        
    print("Extracted text:")
    print("-" * 50)
    print(text)
    print("-" * 50)

    # Optionally save to text file
    output_path = pdf_path.rsplit('.', 1)[0] + '.txt'
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {str(e)}") 