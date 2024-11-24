import os
import requests

def download_file(url, output_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
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

    # Extract filename from the URL
    filename = os.path.basename(url) or "downloaded_file"
    download_file(url, filename)
