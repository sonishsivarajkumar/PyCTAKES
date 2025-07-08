"""Command-line interface for PyCTAKES."""

import json
import sys
from pathlib import Path
from typing import Optional

import click

from . import Pipeline
from .types import Document


@click.group()
@click.version_option()
def main():
    """PyCTAKES: Python-native clinical NLP framework."""
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file for annotations (default: stdout)')
@click.option('--format', 'output_format', type=click.Choice(['json', 'text']), 
              default='json', help='Output format')
@click.option('--config', type=click.Path(exists=True, path_type=Path),
              help='Pipeline configuration file')
@click.option('--pipeline', type=click.Choice(['default', 'fast', 'basic']),
              default='default', help='Pipeline type to use')
def annotate(input_file: Path, output: Optional[Path], output_format: str, 
             config: Optional[Path], pipeline: str):
    """Annotate a single clinical text file."""
    
    # Load configuration if provided
    pipeline_config = {}
    if config:
        with open(config) as f:
            pipeline_config = json.load(f)
    
    # Initialize pipeline with selected type
    if pipeline == 'fast':
        pipeline_instance = Pipeline.create_fast_pipeline(pipeline_config)
    elif pipeline == 'basic':
        pipeline_instance = Pipeline.create_basic_pipeline(pipeline_config)
    else:
        pipeline_instance = Pipeline.create_default_clinical_pipeline(pipeline_config)
    
    # Read input text
    text = input_file.read_text(encoding='utf-8')
    
    # Process the text
    try:
        result = pipeline_instance.process_text(text, doc_id=str(input_file))
        
        # Format output
        if output_format == 'json':
            output_data = {
                'document_id': result.document.doc_id,
                'text': result.document.text,
                'processing_time': result.processing_time,
                'annotations': [
                    {
                        'start': ann.start,
                        'end': ann.end,
                        'text': ann.text,
                        'type': ann.annotation_type.value,
                        'confidence': ann.confidence,
                        'metadata': ann.metadata
                    }
                    for ann in result.document.annotations
                ],
                'errors': result.errors
            }
            output_text = json.dumps(output_data, indent=2, ensure_ascii=False)
        else:
            # Simple text format
            output_lines = [f"Document: {result.document.doc_id}"]
            output_lines.append(f"Processing time: {result.processing_time:.3f}s")
            output_lines.append(f"Annotations: {len(result.document.annotations)}")
            output_lines.append("")
            
            for ann in result.document.annotations:
                output_lines.append(
                    f"{ann.start}-{ann.end}: {ann.text} "
                    f"[{ann.annotation_type.value}] ({ann.confidence:.2f})"
                )
            
            if result.errors:
                output_lines.append("\nErrors:")
                output_lines.extend(result.errors)
            
            output_text = "\n".join(output_lines)
        
        # Write output
        if output:
            output.write_text(output_text, encoding='utf-8')
            click.echo(f"Annotations written to {output}")
        else:
            click.echo(output_text)
            
    except Exception as e:
        click.echo(f"Error processing {input_file}: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--output-dir', '-o', type=click.Path(path_type=Path), required=True,
              help='Output directory for annotations')
@click.option('--pattern', default='*.txt', help='File pattern to match')
@click.option('--config', type=click.Path(exists=True, path_type=Path),
              help='Pipeline configuration file')
@click.option('--parallel', is_flag=True, help='Process files in parallel')
def batch_process(input_dir: Path, output_dir: Path, pattern: str, 
                  config: Optional[Path], parallel: bool):
    """Process multiple files in a directory."""
    
    # Load configuration if provided
    pipeline_config = {}
    if config:
        with open(config) as f:
            pipeline_config = json.load(f)
    
    # Find input files
    input_files = list(input_dir.glob(pattern))
    if not input_files:
        click.echo(f"No files found matching pattern '{pattern}' in {input_dir}")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = Pipeline(config=pipeline_config)
    
    # Process files
    click.echo(f"Processing {len(input_files)} files...")
    
    with click.progressbar(input_files, label="Processing") as files:
        for input_file in files:
            try:
                text = input_file.read_text(encoding='utf-8')
                result = pipeline.process_text(text, doc_id=str(input_file))
                
                # Write output
                output_file = output_dir / f"{input_file.stem}_annotations.json"
                output_data = {
                    'document_id': result.document.doc_id,
                    'text': result.document.text,
                    'processing_time': result.processing_time,
                    'annotations': [
                        {
                            'start': ann.start,
                            'end': ann.end,
                            'text': ann.text,
                            'type': ann.annotation_type.value,
                            'confidence': ann.confidence,
                            'metadata': ann.metadata
                        }
                        for ann in result.document.annotations
                    ],
                    'errors': result.errors
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                click.echo(f"Error processing {input_file}: {e}", err=True)
    
    click.echo(f"Processing complete. Results saved to {output_dir}")


@main.command()
@click.option('--host', default='localhost', help='Host to run the server on')
@click.option('--port', default=8000, help='Port to run the server on')
@click.option('--config', type=click.Path(exists=True, path_type=Path),
              help='Pipeline configuration file')
def serve(host: str, port: int, config: Optional[Path]):
    """Start PyCTAKES as a REST API server."""
    try:
        import uvicorn
        from .api import create_app
    except ImportError:
        click.echo("FastAPI and uvicorn are required to run the server.", err=True)
        click.echo("Install with: pip install 'pyctakes[api]'", err=True)
        sys.exit(1)
    
    # Load configuration if provided
    pipeline_config = {}
    if config:
        with open(config) as f:
            pipeline_config = json.load(f)
    
    app = create_app(pipeline_config)
    
    click.echo(f"Starting PyCTAKES server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main()
