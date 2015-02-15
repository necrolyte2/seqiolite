from setuptools import setup, find_packages

from seqiolite import __version__

setup(
    name = 'seqiolite',
    version = __version__,
    packages = find_packages(),
    setup_requires = [
    ],
    tests_require = [
    ],
    install_requires = [],
    author = 'Tyghe Vallard',
    author_email = 'vallardt@gmail.com',
    description = 'Very quick and simple fasta/fastq file parsing',
    license = 'GPL v2',
    keywords = 'fasta, fastq',
    url = 'https://github.com/necrolyte2/seqiolite',
)
