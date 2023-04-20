from setuptools import setup, find_packages

setup(
    name='arxiv-latex-merger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'arxiv-latex-merger = arxiv_latex_merger.cli:cli',
        ],
    },
)
