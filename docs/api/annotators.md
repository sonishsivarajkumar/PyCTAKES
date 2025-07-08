# Annotators API Reference

PyTAKES provides a comprehensive set of annotators for clinical natural language processing.

## Base Annotator

### `class BaseAnnotator`

Abstract base class for all PyTAKES annotators.

**Methods:**
- `__init__()`: Initialize annotator
- `process(doc)`: Process document and return annotated document

## Tokenization

### `class TokenizationAnnotator(BaseAnnotator)`

Handles sentence segmentation and tokenization of clinical text.

**Parameters:**
- `backend` (str): Backend to use ("spacy", "stanza", "rule_based")
- `model` (str): Model name for spacy/stanza backends

**Methods:**
- `process(doc)`: Add sentences and tokens to document

### `class ClinicalSentenceSegmenter`

Clinical-aware sentence segmentation.

**Features:**
- Respects medical abbreviations
- Handles clinical note formatting
- Configurable sentence boundary detection

### `class ClinicalTokenizer`

Advanced tokenization for clinical text.

**Features:**
- POS tagging and lemmatization
- Clinical pattern recognition
- Multiple backend support

## Section Detection

### `class SectionAnnotator(BaseAnnotator)`

Base class for section detection.

### `class ClinicalSectionAnnotator(SectionAnnotator)`

Identifies clinical document sections.

**Detected Sections:**
- Chief Complaint
- History of Present Illness
- Past Medical History
- Medications
- Physical Examination
- Assessment and Plan

## Named Entity Recognition

### `class NERAnnotator(BaseAnnotator)`

Base class for named entity recognition.

### `class ClinicalNERAnnotator(NERAnnotator)`

Clinical entity recognition with hybrid approach.

**Parameters:**
- `approach` (str): "rule_based" or "model_based"
- `model_name` (str): Model for model-based approach
- `custom_patterns` (dict): Custom entity patterns

**Entity Types:**
- MEDICATION
- CONDITION
- SYMPTOM
- ANATOMY
- PROCEDURE
- TEST_RESULT

### `class SimpleClinicalNER(NERAnnotator)`

Fast pattern-based entity recognition.

**Features:**
- High-speed processing
- Pattern matching
- Optimized for speed over accuracy

## Assertion Detection

### `class AssertionAnnotator(BaseAnnotator)`

Base class for assertion detection.

### `class NegationAssertionAnnotator(AssertionAnnotator)`

pyConText-style assertion and negation detection.

**Parameters:**
- `window_size` (int): Context window size
- `custom_negation_terms` (list): Additional negation terms
- `custom_uncertainty_terms` (list): Additional uncertainty terms

**Assertion Types:**
- Polarity: POSITIVE, NEGATIVE
- Uncertainty: CERTAIN, UNCERTAIN
- Temporality: PRESENT, PAST, FUTURE
- Experiencer: PATIENT, FAMILY, OTHER

## UMLS Concept Mapping

### `class UMLSAnnotator(BaseAnnotator)`

Base class for UMLS concept mapping.

### `class UMLSConceptMapper(UMLSAnnotator)`

Maps entities to UMLS concepts.

**Parameters:**
- `umls_path` (str): Path to UMLS data
- `similarity_threshold` (float): Minimum similarity score
- `max_candidates` (int): Maximum candidate concepts

### `class SimpleDictionaryMapper(UMLSAnnotator)`

Fast dictionary-based concept mapping.

**Parameters:**
- `dictionary_path` (str): Path to concept dictionary
- `similarity_threshold` (float): Minimum similarity score

## Usage Examples

### Tokenization

```python
from pytakes.annotators.tokenization import TokenizationAnnotator

# Create annotator
annotator = TokenizationAnnotator(backend="spacy")

# Process document
doc = annotator.process(doc)

# Access results
for sentence in doc.sentences:
    print(f"Sentence: {sentence.text}")
    for token in sentence.tokens:
        print(f"  Token: {token.text} ({token.pos})")
```

### Named Entity Recognition

```python
from pytakes.annotators.ner import ClinicalNERAnnotator

# Rule-based NER
ner = ClinicalNERAnnotator(approach="rule_based")
doc = ner.process(doc)

# Model-based NER
ner = ClinicalNERAnnotator(
    approach="model_based",
    model_name="en_ner_bc5cdr_md"
)
doc = ner.process(doc)

# Access entities
for entity in doc.entities:
    print(f"Entity: {entity.text} ({entity.label}) at {entity.start}-{entity.end}")
```

### Assertion Detection

```python
from pytakes.annotators.assertion import NegationAssertionAnnotator

# Create assertion annotator
assertion = NegationAssertionAnnotator()
doc = assertion.process(doc)

# Check assertions
for entity in doc.entities:
    if hasattr(entity, 'assertion'):
        print(f"{entity.text}: {entity.assertion.polarity}")
```

### Section Detection

```python
from pytakes.annotators.sections import ClinicalSectionAnnotator

# Create section annotator
sections = ClinicalSectionAnnotator()
doc = sections.process(doc)

# Access sections
for section in doc.sections:
    print(f"Section: {section.section_type} ({section.start}-{section.end})")
```

### UMLS Concept Mapping

```python
from pytakes.annotators.umls import UMLSConceptMapper

# Create UMLS mapper
umls = UMLSConceptMapper()
doc = umls.process(doc)

# Access concepts
for entity in doc.entities:
    if hasattr(entity, 'umls_concept'):
        concept = entity.umls_concept
        print(f"{entity.text} -> {concept.cui} ({concept.preferred_term})")
```

## Custom Annotators

### Creating Custom Annotators

```python
from pytakes.annotators.base import BaseAnnotator
from pytakes.types import Document, Annotation

class CustomAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = kwargs
    
    def process(self, doc: Document) -> Document:
        # Your custom processing logic
        
        # Example: Add custom annotation
        annotation = Annotation(
            start=0,
            end=len(doc.text),
            text=doc.text,
            label="CUSTOM",
            confidence=1.0
        )
        doc.annotations.append(annotation)
        
        return doc
```

### Using Custom Annotators

```python
from pytakes.pipeline import Pipeline

# Create pipeline with custom annotator
pipeline = Pipeline()
pipeline.add_annotator(CustomAnnotator(param1="value1"))

# Process text
result = pipeline.process_text("Some clinical text")
```

## Annotator Configuration

### Tokenization Configuration

```python
# spaCy backend
tokenizer = TokenizationAnnotator(
    backend="spacy",
    model="en_core_web_sm"
)

# Stanza backend
tokenizer = TokenizationAnnotator(
    backend="stanza",
    model="en"
)

# Rule-based backend
tokenizer = TokenizationAnnotator(
    backend="rule_based"
)
```

### NER Configuration

```python
# Rule-based with custom patterns
ner = ClinicalNERAnnotator(
    approach="rule_based",
    custom_patterns={
        "MEDICATION": ["aspirin", "ibuprofen"],
        "CONDITION": ["diabetes", "hypertension"]
    }
)

# Model-based with specific model
ner = ClinicalNERAnnotator(
    approach="model_based",
    model_name="en_ner_bc5cdr_md"
)
```

### Assertion Configuration

```python
# Custom assertion rules
assertion = NegationAssertionAnnotator(
    window_size=10,
    custom_negation_terms=["denies", "negative for"],
    custom_uncertainty_terms=["possible", "likely"]
)
```

## Error Handling

```python
from pytakes.annotators.base import AnnotationError

try:
    doc = annotator.process(doc)
except AnnotationError as e:
    print(f"Annotation failed: {e}")
    # Handle gracefully
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tips

1. **Choose appropriate backends**: spaCy for speed, Stanza for accuracy
2. **Use rule-based for simple tasks**: Faster than model-based approaches
3. **Configure entity types**: Limit NER to needed entity types
4. **Adjust window sizes**: Smaller windows for assertion detection are faster
5. **Enable caching**: For UMLS lookups in production
