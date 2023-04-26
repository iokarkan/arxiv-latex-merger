#!/usr/bin/env python3

__version__='0.2.0'
__author__='iokarkan'

import argparse
from .merger import merge_tex_files, find_main_tex_file
from .downloader import download_arxiv_source_files, download_random_arxiv_papers
from .demacro import LatexDemacro
import shutil
from pathlib import Path

def main(args):
    print(f"arxiv_latex_merger {__version__}")

    if args.arxiv_codes:
        for code in args.arxiv_codes:
            download_arxiv_source_files(code)

            main_tex_path = find_main_tex_file(code, accept_latin1=args.accept_latin1)
            output_tex_path = f'{code}_merged.tex'

            merged_tex_content = merge_tex_files(main_tex_path)

            with open(output_tex_path, 'w') as output_file:
                output_file.write(merged_tex_content)

            print(f'Merged .tex file saved to {output_tex_path}')
    else:
        print(f"Downloading {args.n_random} random arXiv paper(s)...")
        args.arxiv_codes = download_random_arxiv_papers(args.n_random)

    for code in args.arxiv_codes:
        main_tex_path = find_main_tex_file(code)
        output_tex_path = f'{code}_merged.tex'

        # if args.remove_src:
        #     shutil.rmtree(Path(f"./{main_tex_path}"))

        try:
            merged_tex_content = merge_tex_files(main_tex_path, remove_src=args.remove_src)
            with open(f"{code}_merged.tex", "w") as output_file:
                output_file.write(merged_tex_content)
            print(f"{code} file saved to {code}_merged.tex.")
            
        except Exception as e:
            print(f"Could not merge files for {code}: {e}")

        if args.demacro:
            print(f"WARNING: Using experimental 'demacro' processing...")
            input_tex_path = output_tex_path
            output_tex_path = f"{code}_merged_clean.tex"
            demacro_f = LatexDemacro(inp=input_tex_path, out=output_tex_path)

            try:
                merged_clean = demacro_f.process()
                with open(f"{code}_merged_clean.tex", "w") as output_file:
                    output_file.write(merged_clean)
                print(f"{code} file saved to {output_tex_path}.")

            except Exception as e:
                print(f"Could not demacro files for {code}: {e}")
            
        print(f"Finished processing {code}.")


def cli():
    parser = argparse.ArgumentParser(description='Merge LaTeX files from arXiv source.')
    parser.add_argument('--arxiv_codes', nargs='+', default=[], help='The arXiv code(s) for the paper(s).')
    parser.add_argument('--n_random', default=1, help='Fetch n random papers.')
    parser.add_argument('--demacro', action='store_true', default=False, help='(Experimental/Buggy) Attempt to de-macro custom commands defined in the merged file.')
    parser.add_argument('--remove_src', action='store_true', default=False, help='Remove source folder after successful merging.')
    parser.add_argument('--accept_latin1', action='store_true', default=False, help='Accept files that seem encoded with latin-1.')
    args = parser.parse_args()
    main(args)
