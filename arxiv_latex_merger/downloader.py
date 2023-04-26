import os
import tarfile
import arxiv
from pathlib import Path
from tqdm import tqdm
import requests

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

import random

def download_random_arxiv_papers(n=1):
    
    def generate_random_arxiv_id():
        year = str(random.randint(1991, 2022))[-2:]  # arXiv was launched in 1991, change the end year as needed
        month = str(random.randint(1, 12)).rjust(2,"0")
        number = str(random.randint(1, 1412)).rjust(4,"0")  # Choose 28 to avoid issues with months having less than 31 days
        id_part = str(random.randint(1, 2))
        arxiv_id = f"{year}{month}.{number}v{id_part}"
        return arxiv_id

    def is_valid_arxiv_id(arxiv_id):
        url = f"https://arxiv.org/abs/{arxiv_id}"
        response = requests.get(url)
        return response.status_code == 200

    def find_valid_arxiv_id():
        while True:
            random_arxiv_id = generate_random_arxiv_id()
            if is_valid_arxiv_id(random_arxiv_id):
                return random_arxiv_id

    random_papers = arxiv.Search(id_list=[find_valid_arxiv_id() for _ in tqdm(range(int(n)), 
                                                                              desc=f"Generating {n} random arXiv codes...", 
                                                                              unit="code")],
                                max_results=n,
                                sort_by = arxiv.SortCriterion.SubmittedDate)
    arxiv_codes = []
    for paper in random_papers.results():
        arxiv_code = paper.entry_id.rsplit('/', 1)[-1]
        print(f"Downloading source files for paper: {arxiv_code}")
        download_arxiv_source_files(arxiv_code)
        arxiv_codes.append(arxiv_code)
    
    return arxiv_codes


