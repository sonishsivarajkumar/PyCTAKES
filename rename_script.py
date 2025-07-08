#!/usr/bin/env python3
"""
Comprehensive script to rename PyCTAKES to PyCTAKES throughout the codebase.
"""

import os
import re
from pathlib import Path

def rename_in_file(file_path, replacements):
    """Apply text replacements in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def main():
    # Define all the replacements needed
    replacements = {
        # Package names
        'pyctakes': 'pyctakes',
        'PyCTAKES': 'PyCTAKES',
        
        # Import statements
        'import pyctakes': 'import pyctakes',
        'from pyctakes': 'from pyctakes',
        
        # URLs and references
        'sonishsivarajkumar/PyCTAKES': 'sonishsivarajkumar/PyCTAKES',
        'pyctakes.readthedocs.io': 'pyctakes.readthedocs.io',
        'pypi.org/project/pyctakes': 'pypi.org/project/pyctakes',
        
        # CLI commands
        'pyctakes process': 'pyctakes process',
        'pyctakes annotate': 'pyctakes annotate',
        'pyctakes configure': 'pyctakes configure',
        'pyctakes info': 'pyctakes info',
        'pyctakes demo': 'pyctakes demo',
        
        # Entry points and module references
        '"pyctakes[': '"pyctakes[',
        '--cov=pyctakes': '--cov=pyctakes',
        'src/pyctakes': 'src/pyctakes',
        'mypy src/pyctakes': 'mypy src/pyctakes',
        
        # Documentation and comments
        'PyCTAKES CI/CD': 'PyCTAKES CI/CD',
        'PyCTAKES Development Environment': 'PyCTAKES Development Environment',
        'PyCTAKES Documentation': 'PyCTAKES Documentation',
        'Command-line interface for PyCTAKES': 'Command-line interface for PyCTAKES',
        'Core PyCTAKES pipeline': 'Core PyCTAKES pipeline',
        'Main PyCTAKES processing': 'Main PyCTAKES processing',
        'PyCTAKES annotators': 'PyCTAKES annotators',
        'PyCTAKES: Python-native': 'PyCTAKES: Python-native',
        'Types of annotations supported by PyCTAKES': 'Types of annotations supported by PyCTAKES',
        'Base annotation class for all PyCTAKES': 'Base annotation class for all PyCTAKES',
        'Base class for all PyCTAKES annotators': 'Base class for all PyCTAKES annotators',
        'PyCTAKES clinical NLP': 'PyCTAKES clinical NLP',
        'Test configuration for PyCTAKES': 'Test configuration for PyCTAKES',
        'Quick verification script for PyCTAKES': 'Quick verification script for PyCTAKES',
        'Testing PyCTAKES v1.0': 'Testing PyCTAKES v1.0',
        'PyCTAKES v1.0 implementation': 'PyCTAKES v1.0 implementation',
        'Contributing to PyCTAKES': 'Contributing to PyCTAKES',
        'PyCTAKES Roadmap': 'PyCTAKES Roadmap',
        'PyCTAKES Deployment Status': 'PyCTAKES Deployment Status',
        
        # Specific API and variable references
        'pipeline: PyCTAKES pipeline': 'pipeline: PyCTAKES pipeline',
        'pyctakes.create_': 'pyctakes.create_',
        'pip install pyctakes': 'pip install pyctakes',
    }
    
    # Define file patterns to process
    file_patterns = [
        '**/*.py',
        '**/*.md', 
        '**/*.yml',
        '**/*.yaml',
        '**/*.json',
        '**/*.toml',
        '**/*.txt',
        '**/*.rst'
    ]
    
    # Directories to skip
    skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'site'}
    
    # Get all files to process
    files_to_process = []
    for pattern in file_patterns:
        for file_path in Path('.').rglob(pattern):
            if not any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                files_to_process.append(file_path)
    
    # Process each file
    updated_count = 0
    for file_path in files_to_process:
        if rename_in_file(file_path, replacements):
            updated_count += 1
    
    print(f"\nCompleted! Updated {updated_count} files out of {len(files_to_process)} processed.")

if __name__ == '__main__':
    main()
