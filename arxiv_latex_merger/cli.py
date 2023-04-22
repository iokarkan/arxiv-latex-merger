#!/usr/bin/env python3

__version__='0.1.0'
__author__='iokarkan'

import argparse
from .merger import merge_tex_files, find_main_tex_file
from .downloader import download_arxiv_source_files, download_random_arxiv_papers

def main(arxiv_codes, n_random=None):
    print(f"arxiv_latex_merger {__version__}")

    if arxiv_codes:
        for code in arxiv_codes:
            download_arxiv_source_files(code)

            main_tex_path = find_main_tex_file(code)
            output_tex_path = f'{code}_merged.tex'

            merged_tex_content = merge_tex_files(main_tex_path)

            with open(output_tex_path, 'w') as output_file:
                output_file.write(merged_tex_content)

            print(f'Merged .tex file saved to {output_tex_path}')
    else:
        print(f"Downloading {n_random} random arXiv paper(s)...")
        arxiv_codes = download_random_arxiv_papers(n_random)
        for code in arxiv_codes:
            main_tex_path = find_main_tex_file(code)
            output_tex_path = f'{code}_merged.tex'

            merged_tex_content = merge_tex_files(main_tex_path)

            with open(output_tex_path, 'w') as output_file:
                output_file.write(merged_tex_content)

            print(f'Merged .tex file saved to {output_tex_path}')
def cli():
    parser = argparse.ArgumentParser(description='Merge LaTeX files from arXiv source.')
    parser.add_argument('--arxiv_codes', nargs='+', default=[], help='The arXiv code(s) for the paper(s).')
    parser.add_argument('--n_random', default=1, help='Fetch n random papers.')
    args = parser.parse_args()
    main(args.arxiv_codes, n_random=args.n_random)
