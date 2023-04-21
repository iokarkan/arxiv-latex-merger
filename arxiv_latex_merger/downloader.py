import os
import tarfile
import arxiv
from pathlib import Path
from tqdm import tqdm

def download_arxiv_source_files(arxiv_code):
    output_dir = arxiv_code

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Use arxiv API to get the paper object
    papers = arxiv.Search(id_list=[arxiv_code]).results()
    paper = next(papers)

    # Download the source files using the download_source method
    paper.download_source(dirpath=output_dir, filename=f"{arxiv_code}.tar.gz")

    # Extract the tar file to the output directory
    tar_file = os.path.join(output_dir, f"{arxiv_code}.tar.gz")
    with tarfile.open(tar_file, "r:gz") as tar:
        members = tar.getmembers()
        progress_bar = tqdm(total=len(members), unit="file", desc=f"Extracting source files for {arxiv_code}")
        for member in members:
            tar.extract(member, output_dir)
            progress_bar.update(1)
        progress_bar.close()

    # Remove the tar file
    os.remove(tar_file)

    print(f"Successfully downloaded and extracted source files to {output_dir} directory")
