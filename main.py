import logging
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any
from src.stylometric_analysis_app import StylometricAnalysisApp

logger = logging.getLogger(__name__)

def main():
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Analyze PDF document style')
        parser.add_argument('pdf_path', help='Path to PDF file')
        parser.add_argument('--output', help='Output file path')
        parser.add_argument('--format', choices=['dict', 'json', 'pretty_json'], default='dict',
                          help='Output format')
        args = parser.parse_args()

        # Initialize and run analysis
        app = StylometricAnalysisApp()
        logger.info(f"Processing document: {args.pdf_path}")
        results = app.analyze_document(args.pdf_path, args.format)

        # Handle output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                if isinstance(results, str):
                    f.write(results)
                else:
                    json.dump(results, f, indent=2)
            print(f"Results saved to: {args.output}")
        else:
            print(json.dumps(results, indent=2))

    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")

if __name__ == "__main__":
    main()
