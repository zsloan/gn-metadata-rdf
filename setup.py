import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gn_metadata_to_rdf-zsloan",
    version="0.0.1",
    author="Zachary Sloan",
    author_email="zachary.a.sloan@gmail.com",
    description="A command line tool for converting GeneNetwork metadata to RDF triples",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zsloan/gn-metadata-rdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.2',
    entry_points = {
        'console_scripts': ['gn-metadata-to-rdf=gn_to_rdf.main:cli']
    },
)