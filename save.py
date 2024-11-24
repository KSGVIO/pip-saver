import os
import requests

def create_folder(folder_name):
    """Create a folder if it doesn't already exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder created: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")

def download_file(url, folder_name):
    """Download the file from the given URL and save it in the specified folder."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Extract the filename from the URL
        filename = os.path.basename(url) or "downloaded_file"
        output_path = os.path.join(folder_name, filename)

        # Write the file to the folder
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File downloaded successfully: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file. Error: {e}")

if __name__ == "__main__":
    # Prompt the user for the URL
    url = input("Enter the URL of the file to download: ").strip()
    if not url:
        print("No URL provided. Exiting...")
        exit(1)

    # Fixed folder name
    folder_name = "pip-saver"

    # Create the folder
    create_folder(folder_name)

    # Download the file into the folder
    download_file(url, folder_name)
