# Stilo - Stylometric Analysis Tool

A comprehensive tool for analyzing writing style and document characteristics.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository

2. Install dependencies:
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
pip install -e .
```

3. Usage
Run the setup script to install the package:
```bash
python setup.py
```
Run the app:
```bash
python main.py <path_to_file> --output <path_to_output_file>
```
This will generate a JSON file with the stylometric analysis results.

