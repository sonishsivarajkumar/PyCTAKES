# Annotators API Reference

## Base Annotator

::: pytakes.annotators.base.BaseAnnotator
    options:
      show_source: false
      heading_level: 3

## Tokenization

::: pytakes.annotators.tokenization.TokenizationAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.tokenization.ClinicalSentenceSegmenter
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.tokenization.ClinicalTokenizer
    options:
      show_source: false
      heading_level: 3

## Section Detection

::: pytakes.annotators.sections.SectionAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.sections.ClinicalSectionAnnotator
    options:
      show_source: false
      heading_level: 3

## Named Entity Recognition

::: pytakes.annotators.ner.NERAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.ner.ClinicalNERAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.ner.SimpleClinicalNER
    options:
      show_source: false
      heading_level: 3

## Assertion Detection

::: pytakes.annotators.assertion.AssertionAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.assertion.NegationAssertionAnnotator
    options:
      show_source: false
      heading_level: 3

## UMLS Concept Mapping

::: pytakes.annotators.umls.UMLSAnnotator
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.umls.UMLSConceptMapper
    options:
      show_source: false
      heading_level: 3

::: pytakes.annotators.umls.SimpleDictionaryMapper
    options:
      show_source: false
      heading_level: 3

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
