from setuptools import setup, find_packages

setup(
    name='arxiv-latex-merger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'arxiv==1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'arxiv-latex-merger = arxiv_latex_merger.cli:cli',
        ],
    },
)
