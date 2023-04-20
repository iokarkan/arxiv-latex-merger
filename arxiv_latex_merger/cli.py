#!/usr/bin/env python3

__version__='0.1.0'
__author__='iokarkan'

import argparse
from .merger import merge_tex_files, find_main_tex_file
from .downloader import download_arxiv_source_files

def main(arxiv_codes):
    print(f"arxiv_latex_merger {__version__}")

    for code in arxiv_codes:
        download_arxiv_source_files(code)

        main_tex_path = find_main_tex_file(code)
        output_tex_path = f'{code}_merged.tex'

        merged_tex_content = merge_tex_files(main_tex_path)

        with open(output_tex_path, 'w') as output_file:
            output_file.write(merged_tex_content)

        print(f'Merged .tex file saved to {output_tex_path}')

def cli():
    parser = argparse.ArgumentParser(description='Merge LaTeX files from arXiv source.')
    parser.add_argument('arxiv_codes', nargs='+', default=[], help='The arXiv code(s) for the paper(s).')
    args = parser.parse_args()
    main(args.arxiv_codes)
