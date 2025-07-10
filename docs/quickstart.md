# Quick Start Tutorial

This tutorial will get you up and running with pyCTAKES in just a few minutes.

## Step 1: Installation

First, install pyCTAKES:

```bash
pip install pyctakes
```

For enhanced functionality, also install spaCy:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Step 2: Basic Usage

Let's start with a simple example:

```python
import pyctakes

# Create a pipeline
pipeline = pyctakes.create_default_pipeline()

# Sample clinical text
clinical_text = """
CHIEF COMPLAINT: Chest pain

HISTORY OF PRESENT ILLNESS:
Patient is a 65-year-old male with diabetes and hypertension.
He presents with acute onset chest pain radiating to left arm.
Patient denies shortness of breath, nausea, or diaphoresis.

MEDICATIONS:
1. Metformin 500mg twice daily
2. Lisinopril 10mg daily
3. Aspirin 81mg daily
"""

# Process the text
result = pipeline.process_text(clinical_text, doc_id="example_001")

# Display results
print(f"Processing time: {result.processing_time:.3f} seconds")
print(f"Total annotations: {len(result.document.annotations)}")
```

## Step 3: Exploring Annotations

pyCTAKES produces different types of annotations. Let's examine them:

```python
from pyctakes.types import AnnotationType

# Get different annotation types
sentences = result.document.get_annotations(AnnotationType.SENTENCE)
entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
sections = result.document.get_annotations(AnnotationType.SECTION)

print(f"\nFound {len(sentences)} sentences")
print(f"Found {len(entities)} named entities")
print(f"Found {len(sections)} clinical sections")
```

### Examining Named Entities

```python
print("\nNamed Entities:")
for entity in entities[:10]:  # Show first 10
    assertion = getattr(entity, 'assertion', 'PRESENT')
    print(f"  {entity.text:20} | {entity.entity_type.value:12} | {assertion}")
```

Output:
```
Named Entities:
  Chest pain           | disorder     | PRESENT
  diabetes             | disorder     | PRESENT  
  hypertension         | disorder     | PRESENT
  chest pain           | disorder     | PRESENT
  shortness of breath  | sign_symptom | NEGATED
  nausea               | sign_symptom | NEGATED
  Metformin            | medication   | PRESENT
  Lisinopril           | medication   | PRESENT
  Aspirin              | medication   | PRESENT
```

### Examining Clinical Sections

```python
print("\nClinical Sections:")
for section in sections:
    content_preview = section.text[:50].replace('\n', ' ')
    print(f"  {section.section_type:20} | {content_preview}...")
```

## Step 4: Different Pipeline Types

pyCTAKES offers multiple pipeline configurations:

### Fast Pipeline

For high-speed processing:

```python
# Fast pipeline - optimized for speed
fast_pipeline = pyctakes.create_fast_pipeline()
fast_result = fast_pipeline.process_text(clinical_text)

print(f"Fast processing time: {fast_result.processing_time:.3f} seconds")
```

### Basic Pipeline

For simple use cases:

```python
# Basic pipeline - minimal features
basic_pipeline = pyctakes.create_basic_pipeline()
basic_result = basic_pipeline.process_text(clinical_text)

print(f"Basic processing time: {basic_result.processing_time:.3f} seconds")
```

### Custom Pipeline

Build your own pipeline:

```python
from pyctakes import Pipeline
from pyctakes.annotators import (
    ClinicalTokenizer, 
    ClinicalNERAnnotator, 
    NegationAssertionAnnotator
)

# Create custom pipeline
custom_pipeline = Pipeline()
custom_pipeline.add_annotator(ClinicalTokenizer())
custom_pipeline.add_annotator(ClinicalNERAnnotator())
custom_pipeline.add_annotator(NegationAssertionAnnotator())

custom_result = custom_pipeline.process_text(clinical_text)
```

## Step 5: Command Line Usage

pyCTAKES also provides a command-line interface:

```bash
# Save sample text to file
echo "Patient has diabetes and takes metformin." > sample.txt

# Annotate the file
pyctakes annotate sample.txt --output results.json

# View results
cat results.json
```

### Different output formats

```bash
# Text format
pyctakes annotate sample.txt --format text

# Different pipeline types
pyctakes annotate sample.txt --pipeline fast --format text
pyctakes annotate sample.txt --pipeline basic --output basic_results.json
```

## Step 6: Configuration

Create a configuration file for custom behavior:

```python
# Save as config.json
config = {
    "tokenizer": {
        "backend": "spacy",
        "include_pos": True,
        "include_lemma": True
    },
    "ner": {
        "use_model": True,
        "use_rules": True
    },
    "assertion": {
        "max_scope": 8
    }
}

import json
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
```

Use the configuration:

```bash
pyctakes annotate sample.txt --config config.json --output configured_results.json
```

Or in Python:

```python
configured_pipeline = pyctakes.create_default_pipeline(config)
```

## Step 7: Real-World Example

Let's process a more complex clinical note:

```python
complex_note = """
PATIENT: John Doe
DOB: 01/15/1958
MRN: 123456789

CHIEF COMPLAINT: 
Chest pain and shortness of breath

HISTORY OF PRESENT ILLNESS:
67-year-old male with history of CAD, DM2, and HTN presents with acute onset 
chest pain that began 2 hours ago. Pain is substernal, pressure-like, 9/10 
severity, radiating to left arm. Associated with diaphoresis and nausea.
Patient denies fever, chills, or recent illness.

PAST MEDICAL HISTORY:
1. Coronary artery disease - s/p PCI 2018
2. Diabetes mellitus type 2 - on metformin
3. Hypertension - well controlled
4. Hyperlipidemia

MEDICATIONS:
1. Metformin 1000mg BID
2. Lisinopril 10mg daily
3. Atorvastatin 40mg daily
4. Aspirin 81mg daily
5. Metoprolol 25mg BID

SOCIAL HISTORY:
Former smoker - quit 5 years ago. Denies alcohol or drug use.

ASSESSMENT AND PLAN:
Likely acute coronary syndrome. Recommend urgent cardiology consultation.
Continue home medications. Start heparin protocol.
"""

# Process complex note
result = pipeline.process_text(complex_note, doc_id="complex_case")

# Analyze results
entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
sections = result.document.get_annotations(AnnotationType.SECTION)

print(f"Complex note analysis:")
print(f"  Entities found: {len(entities)}")
print(f"  Sections found: {len(sections)}")

# Group entities by type
from collections import defaultdict
entity_groups = defaultdict(list)
for entity in entities:
    entity_groups[entity.entity_type.value].append(entity.text)

for entity_type, texts in entity_groups.items():
    unique_texts = list(set(texts))
    print(f"  {entity_type}: {len(unique_texts)} unique entities")
```

## Next Steps

Now that you've completed the quick start tutorial, explore these advanced topics:

- **[Pipeline Configuration](user-guide/configuration.md)** - Customize pipeline behavior
- **[Custom Annotators](advanced/custom-annotators.md)** - Build your own annotators
- **[Performance Tuning](advanced/performance.md)** - Optimize for your use case
- **[Examples](examples.md)** - More real-world examples
- **[API Reference](api/pipeline.md)** - Complete API documentation

## Common Patterns

### Processing Multiple Files

```python
import os
from pathlib import Path

# Process all text files in a directory
notes_dir = Path("clinical_notes")
pipeline = pyctakes.create_default_pipeline()

for note_file in notes_dir.glob("*.txt"):
    text = note_file.read_text()
    result = pipeline.process_text(text, doc_id=note_file.stem)
    
    # Save results
    output_file = f"annotations/{note_file.stem}.json"
    # ... save logic here
```

### Error Handling

```python
try:
    result = pipeline.process_text(clinical_text)
    if result.errors:
        print(f"Processing completed with {len(result.errors)} errors:")
        for error in result.errors:
            print(f"  - {error}")
except Exception as e:
    print(f"Pipeline failed: {e}")
```

### Performance Monitoring

```python
import time

start_time = time.time()
result = pipeline.process_text(clinical_text)
end_time = time.time()

print(f"Processing time: {result.processing_time:.3f}s")
print(f"Wall clock time: {end_time - start_time:.3f}s") 
print(f"Annotations per second: {len(result.document.annotations)/result.processing_time:.1f}")
```

You're now ready to use pyCTAKES for your clinical NLP projects!
