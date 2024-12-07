import logging.config
import yaml
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any
from src.stylometric_analysis_app import StylometricAnalysisApp

def setup_logging():
    """Setup logging configuration"""
    config_path = Path(__file__).parent / 'config' / 'logging.yaml'
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Analyze PDF document style')
        parser.add_argument('pdf_path', help='Path to PDF file')
        parser.add_argument('--output', help='Output file path')
        parser.add_argument('--format', 
                          choices=['dict', 'json', 'pretty_json', 'csv', 'ml_json'],
                          default='dict',
                          help='Output format (dict, json, pretty_json, csv, or ml_json)')
        args = parser.parse_args()

        # Initialize and run analysis
        app = StylometricAnalysisApp()
        logger.info(f"Processing document: {args.pdf_path}")
        
        # Handle output path for CSV and ML JSON
        if args.format in ['csv', 'ml_json'] and not args.output:
            output_dir = Path('results')
            output_dir.mkdir(exist_ok=True)
            args.output = str(output_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}")
        
        results = app.analyze_document(args.pdf_path, args.format, args.output)

        # Display results or confirmation
        if isinstance(results, str):
            print(results)  # Print save confirmation
        else:
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        logger.exception("Critical error in application")
        raise SystemExit(1)

if __name__ == "__main__":
    main()