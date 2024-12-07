# Stilo - Stylometric Analysis Tool

A comprehensive tool for analyzing writing style and document characteristics, providing detailed metrics and ML-ready outputs.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Output Formats](#output-formats)
- [Project Structure](#project-structure)
- [Available Metrics](#available-metrics)

## Features

- **Comprehensive Analysis**: Extracts and analyzes multiple aspects of writing style
  - Lexical features (word usage, vocabulary richness)
  - Syntactic patterns (sentence structure, complexity)
  - Structural elements (paragraph organization, text density)
  - Readability metrics (Flesch Reading Ease, Gunning Fog)

- **Multiple Output Formats**: 
  - Detailed JSON reports
  - ML-ready CSV format
  - Human-readable summaries

- **Advanced Metrics**:
  - Style consistency scoring
  - Document complexity analysis
  - Writing pattern detection
  - Vocabulary usage assessment

- **Performance**:
  - Efficient PDF text extraction
  - Parallel processing for large documents
  - Optimized feature calculations

- **Developer-Friendly**:
  - Modular architecture
  - Extensive logging
  - Clear documentation
  - Type-safe implementation



## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stylometrics-analyzer.git
cd stylometrics-analyzer
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
# Install required packages
pip install -r requirements.txt

# Install NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

# Install spaCy model
python -m spacy download en_core_web_sm

# Install the package in development mode
pip install -e .
```

## Usage

### Basic Analysis (Generates both JSON and CSV)
```bash
python -m src.main "<path_to_pdf>"

or

stilo "<path_to_pdf>"

# Creates: 
# - results/analysis_TIMESTAMP.json
# - results/analysis_TIMESTAMP.csv
```
This will create both JSON and CSV files in the results directory with a timestamp.

### Specific Format Output

1. JSON output only:
```bash
python -m src.main "<path_to_pdf>" --format json

or


stilo "<path_to_pdf>" --format json

# Creates: ./results/analysis_TIMESTAMP.json
```

2. CSV output only:
```bash
python -m src.main "<path_to_pdf>" --format csv

or

stilo "<path_to_pdf>" --format csv

# Creates: ./results/analysis_TIMESTAMP.csv
```

## Output Formats

1. **JSON** (default when format specified):
   - Complete analysis with all metrics
   - Formatted for readability (pretty-printed)
   - Includes all features and analysis results

2. **CSV** (optimized for ML):
   - Flattened data structure
   - Key metrics and features only
   - Ready for machine learning or spreadsheet analysis

When no format is specified, both JSON and CSV files are generated automatically.

## Project Structure

```
stylometrics-analyzer/
├── src/                    # Source code
│   ├── main.py            # Entry point
│   ├── features/          # Feature extractors
│   ├── models/            # Analysis models
│   └── utils/             # Utility functions
├── results/               # Output directory
├── tests/                 # Test files
└── docs/                  # Documentation
```

## Available Metrics

See [METRICS_GUIDE.md](METRICS_GUIDE.md) for detailed explanation of:
- Style metrics (complexity, consistency)
- Writing patterns
- Lexical features
- Syntactic features
- Readability scores

## Troubleshooting

1. If you get import errors:
   ```bash
   pip install -e .
   ```

2. If NLTK data is missing:
   ```bash
   python -c "import nltk; nltk.download('all')"
   ```

3. If spaCy model is missing:
   ```bash
   python -m spacy download en_core_web_sm
   ```

