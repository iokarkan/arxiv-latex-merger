import os
import tarfile
import urllib.request
from pathlib import Path
from tqdm import tqdm

def download_arxiv_source_files(arxiv_code):
    url = f"https://arxiv.org/e-print/{arxiv_code}"
    file_name = f"{arxiv_code}.tar"
    output_dir = arxiv_code

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Download the tar file
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        content_length = int(response.getheader('content-length'))
        progress_bar = tqdm(total=content_length, unit='B', unit_scale=True, desc=f'Downloading source files for {arxiv_code}')
        downloaded_size = 0
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded_size += len(chunk)
            progress_bar.update(len(chunk))
        progress_bar.close()

    # Extract the tar file to the output directory
    with tarfile.open(file_name) as tar:
        tar.extractall(output_dir)

    # Delete the tar file
    os.remove(file_name)

    print(f'Successfully downloaded and extracted source files to {output_dir} directory')
