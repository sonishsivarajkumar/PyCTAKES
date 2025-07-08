# Installation Guide

## Requirements

PyTAKES requires Python 3.8 or higher and is tested on:

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Linux, macOS, and Windows

## Basic Installation

### Install from PyPI (Recommended)

```bash
pip install pytakes
```

This installs PyTAKES with basic dependencies for rule-based processing.

### Development Installation

For the latest development version:

```bash
pip install git+https://github.com/sonish777/pytakes.git
```

## Optional Dependencies

PyTAKES supports multiple NLP backends. Install additional packages for enhanced functionality:

### spaCy (Recommended)

For advanced tokenization, POS tagging, and model-based NER:

```bash
# Install spaCy
pip install spacy

# Download English model
python -m spacy download en_core_web_sm

# For clinical models (optional)
pip install scispacy
python -m spacy download en_core_sci_sm
```

### Stanza

Alternative NLP backend:

```bash
pip install stanza
```

### UMLS Integration

For comprehensive concept mapping:

```bash
pip install quickumls
# Requires UMLS license and setup
```

## Complete Installation

For all features:

```bash
# Install with all optional dependencies
pip install pytakes[all]

# Or install components separately
pip install pytakes spacy scispacy stanza
python -m spacy download en_core_web_sm
python -m spacy download en_core_sci_sm
```

## Verification

Verify your installation:

```python
import pytakes

# Test basic functionality
pipeline = pytakes.create_basic_pipeline()
result = pipeline.process_text("Patient has diabetes.")
print(f"Found {len(result.document.annotations)} annotations")
```

## Docker Installation

Run PyTAKES in Docker:

```bash
# Pull the image
docker pull sonish777/pytakes:latest

# Run interactively
docker run -it sonish777/pytakes:latest python

# Process a file
docker run -v $(pwd):/data sonish777/pytakes:latest \
  pytakes annotate /data/clinical_note.txt
```

## Troubleshooting

### Common Issues

**1. spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**2. Permission errors**
```bash
pip install --user pytakes
```

**3. Environment conflicts**
```bash
# Use virtual environment
python -m venv pytakes_env
source pytakes_env/bin/activate  # Linux/Mac
# or pytakes_env\Scripts\activate  # Windows
pip install pytakes
```

### Platform-Specific Notes

**macOS Apple Silicon (M1/M2)**
```bash
# Install with conda for better compatibility
conda install pytakes -c conda-forge
```

**Windows**
```bash
# Use conda on Windows for easier dependency management
conda install pytakes -c conda-forge
```

**Linux**
```bash
# May need additional system dependencies
sudo apt-get install python3-dev build-essential
pip install pytakes
```

## Performance Optimization

For optimal performance:

1. **Install spaCy models**: Significantly improves NER accuracy
2. **Use SSD storage**: Faster model loading
3. **Allocate sufficient RAM**: 4GB+ recommended for large models
4. **GPU support**: Install CUDA-compatible packages for transformer models

## Next Steps

- [Quick Start Tutorial](quickstart.md)
- [Configuration Guide](user-guide/configuration.md)
- [Examples](examples.md)
