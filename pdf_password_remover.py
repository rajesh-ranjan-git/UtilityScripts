"""
PDF Password Remover Script
Removes password protection from a PDF file.
Requires: pip install pypdf
"""

from pypdf import PdfReader, PdfWriter
import sys
import os


def remove_pdf_password(input_path, output_path, password):
    """
    Remove password protection from a PDF file.
    
    Args:
        input_path (str): Path to the password-protected PDF
        output_path (str): Path where the unlocked PDF will be saved
        password (str): Password to decrypt the PDF
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the encrypted PDF
        reader = PdfReader(input_path)
        
        # Check if PDF is encrypted
        if not reader.is_encrypted:
            print(f"PDF '{input_path}' is not password protected.")
            return False
        
        # Decrypt the PDF with the password
        if not reader.decrypt(password):
            print("Incorrect password. Failed to decrypt PDF.")
            return False
        
        # Create a writer object
        writer = PdfWriter()
        
        # Copy all pages to the writer
        for page in reader.pages:
            writer.add_page(page)
        
        # Write the unencrypted PDF to output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Successfully removed password protection.")
        print(f"Unlocked PDF saved to: {output_path}")
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def validate_paths(input_path, output_path):
    """
    Validate input and output file paths.
    
    Args:
        input_path (str): Input PDF file path
        output_path (str): Output PDF file path
    
    Returns:
        bool: True if paths are valid, False otherwise
    """
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        return False
    
    # Check if input file is a PDF
    if not input_path.lower().endswith('.pdf'):
        print("Error: Input file must be a PDF.")
        return False
    
    # Check if output path is valid
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        return False
    
    return True


def main():
    """
    Main function to handle command-line execution.
    """
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_pdf> <output_pdf> <password>")
        print("\nExample:")
        print("  python script.py protected.pdf unlocked.pdf mypassword123")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    password = sys.argv[3]
    
    # Validate paths
    if not validate_paths(input_path, output_path):
        sys.exit(1)
    
    # Remove password
    success = remove_pdf_password(input_path, output_path, password)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()