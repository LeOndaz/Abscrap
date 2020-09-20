import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapit",  # Replace with your own username
    version="1.0.1",
    author="Ahmed Ibrahim",
    author_email="ahmeddark369@gmail.com",
    description="A scraper for websites using config files created for those sites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/github/scrapit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
