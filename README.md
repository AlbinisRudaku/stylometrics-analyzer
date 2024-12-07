# Stilo - Stylometric Analysis Tool

A comprehensive tool for analyzing writing style and document characteristics, providing detailed metrics and ML-ready outputs.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AlbinisRudaku/stylometrics-analyzer.git
cd stylometrics-analyzer
```

2. Create and activate a virtual environment (optional):
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

### Output Formats

1. Pretty JSON output (default, without --format flag):
```bash
python -m src.main "<path_to_pdf>" --output results/analysis.json
```

2. CSV format (for ML/data analysis, requires --format flag) (Still in BETA, data may be incomplete):
```bash
python -m src.main "<path_to_pdf>" --format csv --output results/analysis.csv
```
or
```bash
stilo "<path_to_pdf>" --format csv --output results/analysis.csv
```

3. ML-friendly JSON format (requires --format flag, recommended):
```bash
python -m src.main "<path_to_pdf>" --format ml_json --output results/ml_features.json
```
or
```bash
stilo "<path_to_pdf>" --format ml_json --output results/ml_features.json
```

### Examples

Analyze a PDF file:
```bash
python -m src.main "./documents/sample.pdf" --output ./results/analysis.json
```
or
```bash
stilo "./documents/sample.pdf" --output ./results/analysis.json
```

Generate CSV for machine learning:
```bash
python -m src.main "./documents/sample.pdf" --format csv --output ./results/features.csv
```
or
```bash
stilo "./documents/sample.pdf" --format csv --output ./results/features.csv
```

## Output Formats Explained

1. **pretty_json**: Complete analysis with all metrics, formatted for readability
2. **csv**: Flattened data structure suitable for ML training or spreadsheet analysis
3. **ml_json**: Curated features specifically formatted for machine learning tasks

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

See METRICS_GUIDE.md for detailed explanation of:
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

