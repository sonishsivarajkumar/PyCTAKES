# PyTAKES (Python-native cTAKES)

**Lead Maintainer:** Sonish Sivarajkumar

## Overview

PyTAKES is an entirely Python-based clinical NLP framework that mirrors and extends Apache cTAKES' rich functionality, while delivering an easy-to-install, easy-to-use package on PyPI. It supports deep end-to-end clinical text processing, from tokenization through UMLS concept mapping, and adds an optional "agentic" LLM layer for smart disambiguation and active learning.

## Quick Start

### Installation

```bash
pip install pytakes
```

### Basic Usage

```python
import pytakes

# Create a default clinical pipeline
pipeline = pytakes.create_default_pipeline()

# Process clinical text
clinical_text = """
Patient is a 65-year-old male with diabetes and hypertension.
He presents with chest pain but denies shortness of breath.
Current medications include metformin and lisinopril.
"""

result = pipeline.process_text(clinical_text)

# Access annotations
entities = result.document.get_annotations("NAMED_ENTITY")
for entity in entities:
    print(f"{entity.text} -> {entity.entity_type}")
```

### Command Line Interface

```bash
# Annotate a clinical text file
pytakes annotate sample_note.txt --output annotations.json

# Use different pipeline types
pytakes annotate sample_note.txt --pipeline fast --format text
pytakes annotate sample_note.txt --pipeline basic --config config.json
```

## Key Features

### Core Clinical NLP Pipeline ✅
- **Sentence Segmentation**: Clinical-aware sentence boundary detection
- **Tokenization**: Clinical text tokenization with POS tagging and lemmatization
- **Section Detection**: Automatic detection of clinical sections (History, Medications, Assessment, etc.)
- **Named Entity Recognition**: Medical entity extraction (disorders, medications, procedures, anatomy)
- **Negation & Assertion**: pyConText-style negation and assertion detection  
- **Concept Mapping**: UMLS concept mapping with CUI normalization

### Multiple Pipeline Configurations
- **Default Pipeline**: Full clinical NLP pipeline with all features
- **Fast Pipeline**: Optimized for speed with rule-based components
- **Basic Pipeline**: Minimal pipeline for simple use cases
- **Custom Pipeline**: Build your own with configurable annotators

### Clinical Text Processing
- spaCy and Stanza backend support for linguistic processing
- Clinical abbreviation and terminology handling
- Robust handling of clinical note formatting and sections
- Configurable rule sets for different clinical domains

### Advanced Features (Planned)
- Relation extraction between clinical entities
- Temporal information extraction
- LLM-powered disambiguation and active learning
- RESTful API service deployment
- Plugin architecture for custom annotators
- Optional multiprocessing or Dask integration for batch processing of large corpora
- Benchmarks included to guide resource planning

### Testing & CI/CD
- Unit and integration tests covering 95%+ of codebase
- Continuous integration on GitHub Actions: linting, type checks, package build, and publish workflow
- Sample clinical datasets (i2b2, MIMIC) for regression testing

### Community & Governance
- Contribution guide with code style, issue templates, and PR checklist
- Slack channel and monthly video calls for roadmap planning
- Transparent governance: core team, advisory board, and community elections

## Configuration

PyTAKES supports flexible configuration through JSON files:

```json
{
  "sentence_segmenter": {
    "backend": "spacy"
  },
  "tokenizer": {
    "backend": "spacy", 
    "include_pos": true,
    "include_lemma": true
  },
  "ner": {
    "use_model": true,
    "use_rules": true,
    "model_name": "en_core_sci_sm"
  },
  "assertion": {
    "max_scope": 10
  },
  "concept_mapping": {
    "use_umls": false,
    "dictionaries": ["disorders", "medications"]
  }
}
```

## Examples

### Custom Pipeline

```python
from pytakes import Pipeline
from pytakes.annotators import ClinicalTokenizer, ClinicalNERAnnotator

# Build custom pipeline
pipeline = Pipeline()
pipeline.add_annotator(ClinicalTokenizer())
pipeline.add_annotator(ClinicalNERAnnotator({"use_rules": True}))

result = pipeline.process_text("Patient takes metformin for diabetes.")
```

### Processing Clinical Sections

```python
import pytakes

clinical_note = """
CHIEF COMPLAINT: Chest pain

MEDICATIONS:
1. Metformin 500mg BID
2. Lisinopril 10mg daily

ASSESSMENT:
Diabetes well controlled.
"""

pipeline = pytakes.create_default_pipeline()
result = pipeline.process_text(clinical_note)

# Get sections
sections = result.document.get_annotations("SECTION")
for section in sections:
    print(f"{section.section_type}: {section.text[:50]}...")

# Get medications
entities = result.document.get_annotations("NAMED_ENTITY")
medications = [e for e in entities if e.entity_type == "MEDICATION"]
for med in medications:
    print(f"Medication: {med.text}")
```

## Development Status

### ✅ Completed (v1.0)
- Core pipeline architecture
- Clinical sentence segmentation and tokenization
- Section detection (Chief Complaint, History, Medications, Assessment, etc.)
- Named Entity Recognition (disorders, medications, procedures, anatomy)
- Negation and assertion detection (pyConText-style)
- Basic UMLS concept mapping
- CLI interface with multiple pipeline types
- Comprehensive test suite

### 🚧 In Progress
- Advanced tokenization features (abbreviation expansion)
- Enhanced concept mapping with additional ontologies
- Performance optimizations
- Documentation and examples

### 📋 Planned (v1.1+)
- Relation extraction between entities
- Temporal information processing
- REST API service
- Docker deployment
- Plugin architecture
- LLM integration for disambiguation

## Roadmap

- **v1.0**: ✅ Core pipeline, concept mapping, assertion/negation, CLI & API
- **v1.1**: Relation extraction, Docker images, performance optimizations  
- **v2.0**: LLM integration, active learning, transformer models
- **Future**: Real-time processing, federated learning, EHR integration

## License

Apache-2.0