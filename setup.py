from setuptools import setup, find_packages

setup(
    name="stilo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "nltk>=3.6.5",
        "PyPDF2>=2.0.0",
        "scikit-learn>=0.24.2",
        "pydantic>=1.8.2",
    ],
    python_requires=">=3.8",
) 