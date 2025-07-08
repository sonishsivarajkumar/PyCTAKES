# Pipeline API Reference

The PyCTAKES pipeline module provides the core functionality for processing clinical text through configurable annotator chains.

## Pipeline Class

### `class Pipeline`

Main pipeline class for clinical text processing.

**Methods:**

- `__init__()`: Initialize empty pipeline
- `add_annotator(annotator)`: Add annotator to pipeline
- `process_text(text)`: Process single text string
- `process_batch(texts)`: Process multiple texts
- `from_config(config)`: Create pipeline from configuration

## Pipeline Factory Functions

### `create_default_pipeline(config=None)`

Create default clinical NLP pipeline with all annotators.

**Parameters:**
- `config` (dict, optional): Configuration dictionary

**Returns:**
- `Pipeline`: Configured pipeline instance

**Includes:**
- Tokenization (spaCy backend)
- Section detection
- Named entity recognition
- Assertion detection
- UMLS concept mapping

### `create_fast_pipeline(config=None)`

Create speed-optimized pipeline with rule-based components.

**Parameters:**
- `config` (dict, optional): Configuration dictionary

**Returns:**
- `Pipeline`: Configured pipeline instance

**Includes:**
- Tokenization (rule-based)
- Named entity recognition (rule-based)
- Basic assertion detection

### `create_basic_pipeline(config=None)`

Create minimal pipeline for simple entity extraction.

**Parameters:**
- `config` (dict, optional): Configuration dictionary

**Returns:**
- `Pipeline`: Configured pipeline instance

**Includes:**
- Tokenization (rule-based)
- Named entity recognition (rule-based)

## Usage Examples

### Basic Pipeline Usage

```python
from pyctakes.pipeline import Pipeline, create_default_pipeline

# Create pipeline
pipeline = create_default_pipeline()

# Process text
result = pipeline.process_text("Patient has diabetes and hypertension.")

# Access results
print(f"Found {len(result.entities)} entities")
for entity in result.entities:
    print(f"- {entity.text} ({entity.label})")
```

### Custom Pipeline

```python
from pyctakes.pipeline import Pipeline
from pyctakes.annotators import TokenizationAnnotator, NERAnnotator

# Create custom pipeline
pipeline = Pipeline()
pipeline.add_annotator(TokenizationAnnotator(backend="spacy"))
pipeline.add_annotator(NERAnnotator(approach="rule_based"))

# Process document
doc = pipeline.process_text("Patient takes aspirin 81mg daily.")
```

### Pipeline Configuration

```python
from pyctakes.pipeline import Pipeline

# Load from configuration file
pipeline = Pipeline.from_config("config.json")

# Load from dictionary
config = {
    "tokenization": {"backend": "spacy"},
    "ner": {"approach": "rule_based"}
}
pipeline = Pipeline.from_config(config)
```

### Batch Processing

```python
from pyctakes.pipeline import Pipeline

pipeline = create_default_pipeline()

# Process multiple texts
texts = [
    "Patient has diabetes.",
    "No history of hypertension.",
    "Takes metformin 500mg twice daily."
]

results = pipeline.process_batch(texts)
for i, result in enumerate(results):
    print(f"Text {i+1}: {len(result.entities)} entities")
```

## Pipeline Methods

### add_annotator(annotator)

Add an annotator to the pipeline.

**Parameters:**
- `annotator`: An instance of a PyCTAKES annotator

**Example:**
```python
from pyctakes.annotators import TokenizationAnnotator

pipeline = Pipeline()
pipeline.add_annotator(TokenizationAnnotator())
```

### process_text(text)

Process a single text string.

**Parameters:**
- `text` (str): The clinical text to process

**Returns:**
- `Document`: Processed document with annotations

**Example:**
```python
doc = pipeline.process_text("Patient has diabetes.")
```

### process_batch(texts)

Process multiple texts in batch.

**Parameters:**
- `texts` (List[str]): List of clinical texts to process

**Returns:**
- `List[Document]`: List of processed documents

**Example:**
```python
docs = pipeline.process_batch(["Text 1", "Text 2"])
```

### from_config(config)

Create pipeline from configuration.

**Parameters:**
- `config` (str or dict): Configuration file path or dictionary

**Returns:**
- `Pipeline`: Configured pipeline instance

**Example:**
```python
pipeline = Pipeline.from_config("my_config.json")
```

## Pipeline Types

### Default Pipeline

Full-featured clinical NLP pipeline with all annotators:

```python
pipeline = create_default_pipeline()
```

**Includes:**
- Tokenization (spaCy backend)
- Section detection
- Named entity recognition
- Assertion detection
- UMLS concept mapping

### Fast Pipeline

Speed-optimized pipeline with rule-based components:

```python
pipeline = create_fast_pipeline()
```

**Includes:**
- Tokenization (rule-based)
- Named entity recognition (rule-based)
- Basic assertion detection

### Basic Pipeline

Minimal pipeline for simple entity extraction:

```python
pipeline = create_basic_pipeline()
```

**Includes:**
- Tokenization (rule-based)
- Named entity recognition (rule-based)

## Error Handling

```python
from pyctakes.pipeline import Pipeline, PipelineError

try:
    pipeline = Pipeline.from_config("invalid_config.json")
    result = pipeline.process_text("Some text")
except PipelineError as e:
    print(f"Pipeline error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

- **Tokenization Backend**: spaCy fastest, Stanza most accurate
- **NER Approach**: Rule-based faster, model-based more accurate
- **Batch Processing**: More efficient for multiple documents
- **Configuration**: Disable unused annotators for better performance
