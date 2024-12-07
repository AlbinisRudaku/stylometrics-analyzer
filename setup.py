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
        "spacy>=3.1.0",
        "textblob>=0.15.3",
        "plotly>=5.3.1",
        "streamlit>=1.24.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
        "rich>=10.0.0",
        "tqdm>=4.62.0",
        "pyyaml>=5.4.1"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'stilo=src.main:main',
        ],
    }
) 