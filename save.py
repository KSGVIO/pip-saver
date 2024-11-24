import os
import requests
from tqdm import tqdm  # Import tqdm for progress bar
import argparse  # For command-line arguments
import sys  # Import sys to use sys.exit()

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Allow redirects and send the headers
        response = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        
        # Check if the URL is valid (status code 200 means successful)
        response.raise_for_status()

        # Extract the filename from the URL
        filename = os.path.basename(url) or "downloaded_file"
        output_path = os.path.join(folder_name, filename)

        # Get the total file size from headers
        total_size = int(response.headers.get('content-length', 0))

        # Use tqdm to display a progress bar
        with open(output_path, "wb") as file, tqdm(
            desc=filename,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                progress_bar.update(len(chunk))
        
        print(f"File downloaded successfully: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file. Error: {e}")

def get_urls_from_input():
    """Prompts the user for URLs and ensures they are properly formatted."""
    urls_input = input("Enter the URLs of the files to download (separated by commas): ").strip()
    
    # Split by comma and strip each URL of any extra spaces or invalid characters
    if not urls_input:
        print("No URLs provided. Exiting...")
        sys.exit(1)

    urls = [url.strip().rstrip(',') for url in urls_input.split(",")]

    # Validate URLs (basic validation to make sure they start with http:// or https://)
    valid_urls = []
    for url in urls:
        if url.startswith("http://") or url.startswith("https://"):
            valid_urls.append(url)
        else:
            print(f"Skipping invalid URL: {url}")

    if not valid_urls:
        print("No valid URLs found. Exiting...")
        sys.exit(1)

    return valid_urls

def pause_program():
    """Pause the program and wait for user input to continue."""
    input("Press Enter to continue...")

def parse_cli_urls(args_urls):
    """Handle URLs from the CLI argument and ensure they are properly cleaned and validated."""
    # If URLs are provided directly via CLI, process them
    urls = []
    for url in args_urls:
        # Clean up any commas or extra spaces and ensure the URL starts with http:// or https://
        cleaned_url = url.strip().rstrip(',')
        if cleaned_url.startswith("http://") or cleaned_url.startswith("https://"):
            urls.append(cleaned_url)
        else:
            print(f"Skipping invalid URL: {cleaned_url}")

    if not urls:
        print("No valid URLs found. Exiting...")
        sys.exit(1)

    return urls

if __name__ == "__main__":
    # Setup argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Download files from URLs.")
    
    # Add the -cli argument
    parser.add_argument("-cli", action="store_true", help="Run in command-line mode to download files.")
    parser.add_argument("urls", nargs="*", help="URLs of the files to download (use space-separated URLs).")

    # Parse arguments
    args = parser.parse_args()

    # Fixed folder name
    folder_name = "pip-saver"

    # Create the folder
    create_folder(folder_name)

    if args.cli:
        # If called with -cli, download all provided URLs
        if not args.urls:
            print("No URLs provided with -cli. Exiting...")
            sys.exit(1)

        print(f"Downloading files in CLI mode...")

        # Handle and clean the URLs passed through CLI
        urls = parse_cli_urls(args.urls)

        # Loop through each URL and download the file
        for url in urls:
            download_file(url, folder_name)

    else:
        # Normal mode - Prompt for URLs
        urls = get_urls_from_input()

        # Loop through each URL and download the file
        for url in urls:
            download_file(url, folder_name)

        # Pause after downloads are complete (optional)
        pause_program()

    # Exit the program after the final pause
    sys.exit(0)
