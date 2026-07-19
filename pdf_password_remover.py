from pypdf import PdfReader, PdfWriter
import os
import getpass


def remove_pdf_password(input_path, output_path, password):
    try:
        reader = PdfReader(input_path)

        if not reader.is_encrypted:
            print(f"[SKIP] {os.path.basename(input_path)} is not password protected.")
            return False

        if reader.decrypt(password) == 0:
            print(f"[FAIL] Incorrect password for {os.path.basename(input_path)}")
            return False

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"[OK] {os.path.basename(input_path)}")
        return True

    except Exception as e:
        print(f"[FAIL] {os.path.basename(input_path)}: {e}")
        return False


def unlock_single():
    input_path = input("\nEnter PDF path: ").strip('"')

    if not os.path.exists(input_path):
        print("File not found.")
        return

    password = getpass.getpass("Enter PDF password: ")

    output_dir = os.path.join(os.path.dirname(input_path), "unlocked")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, os.path.basename(input_path))

    remove_pdf_password(input_path, output_path, password)


def unlock_current_directory():
    current_dir = os.getcwd()

    pdfs = [
        f for f in os.listdir(current_dir)
        if f.lower().endswith(".pdf")
    ]

    if not pdfs:
        print("No PDF files found in current directory.")
        return

    password = getpass.getpass("Enter PDF password: ")

    output_dir = os.path.join(current_dir, "unlocked")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nFound {len(pdfs)} PDF(s).\n")

    success = 0

    for pdf in pdfs:
        input_path = os.path.join(current_dir, pdf)
        output_path = os.path.join(output_dir, pdf)

        if remove_pdf_password(input_path, output_path, password):
            success += 1

    print(f"\nCompleted: {success}/{len(pdfs)} PDFs unlocked.")


def main():
    print("=" * 45)
    print("         PDF Password Remover")
    print("=" * 45)

    print("\nChoose an option:")
    print("1. Unlock a single PDF")
    print("2. Unlock all PDFs in current directory")

    while True:
        choice = input("\nEnter choice (1/2): ").strip()

        if choice == "1":
            unlock_single()
            break
        elif choice == "2":
            unlock_current_directory()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()