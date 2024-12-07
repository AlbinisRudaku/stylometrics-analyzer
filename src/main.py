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
        parser.add_argument('--output', help='Output file path base (without extension)')
        parser.add_argument('--format', 
                          choices=['json', 'csv'],
                          help='Output format (json or csv). If not specified, generates both')
        args = parser.parse_args()

        # Initialize and run analysis
        app = StylometricAnalysisApp()
        logger.info(f"Processing document: {args.pdf_path}")
        
        # Handle output path
        output_dir = Path('results')
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if args.format:
            # Single format output
            extension = '.json' if args.format == 'json' else '.csv'
            output_path = args.output if args.output else str(output_dir / f"analysis_{timestamp}{extension}")
            
            # Get results
            results = app.analyze_document(args.pdf_path, args.format, output_path)
            
            # Save results
            if isinstance(results, str):
                logger.info(results)  # Log CSV save message
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                logger.info(f"Results saved to: {output_path}")
        else:
            # Generate both JSON and CSV
            base_path = args.output if args.output else str(output_dir / f"analysis_{timestamp}")
            
            # Get and save JSON results
            json_results = app.analyze_document(args.pdf_path, 'json')
            json_path = f"{base_path}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_results, f, indent=2)
            logger.info(f"JSON results saved to: {json_path}")
            
            # Get and save CSV results
            csv_path = f"{base_path}.csv"
            app.data_formatter.to_csv(json_results, csv_path)
            logger.info(f"CSV results saved to: {csv_path}")
            
    except Exception as e:
        logger.exception("Critical error in application")
        raise SystemExit(1)

if __name__ == "__main__":
    main()