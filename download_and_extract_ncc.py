import requests
import zipfile
import os

def download_and_extract_ncc(url, save_directory="NCC_PDFs"):
    """
    Downloads the complete series ZIP file from the given URL, extracts its contents,
    and saves the PDF files to a specified local directory.

    Args:
        url (str): The URL of the complete series ZIP file.
        save_directory (str): The name of the directory to save the PDFs to.
                              Defaults to "NCC_PDFs".
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"Created directory: {save_directory}")

    zip_file_name = "NCC_Complete_Series.zip"
    zip_file_path = os.path.join(save_directory, zip_file_name)

    print(f"Attempting to download from: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(zip_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {zip_file_name} to {zip_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return

    print(f"Extracting contents of {zip_file_name}...")
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Get a list of all files in the zip and filter for PDFs
            pdf_files = [name for name in zip_ref.namelist() if name.lower().endswith('.pdf')]

            if not pdf_files:
                print("No PDF files found in the ZIP archive.")
            else:
                for pdf_file in pdf_files:
                    try:
                        # Extract only PDF files
                        zip_ref.extract(pdf_file, save_directory)
                        print(f"Extracted: {pdf_file}")
                    except Exception as e:
                        print(f"Error extracting {pdf_file}: {e}")

        print("Extraction complete.")

    except zipfile.BadZipFile:
        print(f"Error: {zip_file_name} is not a valid ZIP file or is corrupted.")
    except FileNotFoundError:
        print(f"Error: ZIP file not found at {zip_file_path}. It might not have downloaded correctly.")
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")

    finally:
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            print(f"Removed temporary ZIP file: {zip_file_path}")


if __name__ == "__main__":
    
    # URL for the NCC complete series ZIP file
    ncc_zip_url = "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-complete-series-20230501b.zip" 
    # Directory to save the extracted PDFs
    pdf_directory = "NCC_PDFs"
    
    # Call the function to download and extract
    download_and_extract_ncc(ncc_zip_url, save_directory=pdf_directory)