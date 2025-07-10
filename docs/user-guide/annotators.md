# Annotators

pyCTAKES provides a comprehensive set of annotators for clinical natural language processing. Each annotator specializes in extracting specific types of information from clinical text.

## Available Annotators

### TokenizationAnnotator

Handles sentence segmentation and tokenization of clinical text.

**Features:**
- Clinical sentence segmentation (respects medical abbreviations)
- Word tokenization optimized for clinical text
- Multiple backend support (spaCy, Stanza, rule-based)

**Configuration:**
```json
{
  "tokenization": {
    "backend": "spacy",  // or "stanza", "rule_based"
    "model": "en_core_web_sm"
  }
}
```

**Usage:**
```python
from pyctakes.annotators.tokenization import TokenizationAnnotator

annotator = TokenizationAnnotator(backend="spacy")
doc = annotator.process(doc)

# Access tokens and sentences
for sentence in doc.sentences:
    print(f"Sentence: {sentence.text}")
    for token in sentence.tokens:
        print(f"  Token: {token.text}")
```

### SectionAnnotator

Identifies and classifies clinical document sections.

**Detected Sections:**
- Chief Complaint
- History of Present Illness  
- Past Medical History
- Medications
- Allergies
- Social History
- Family History
- Review of Systems
- Physical Examination
- Assessment and Plan
- Discharge Instructions

**Configuration:**
```json
{
  "sections": {
    "custom_patterns": {
      "CUSTOM_SECTION": ["custom header:", "another pattern"]
    }
  }
}
```

**Usage:**
```python
from pyctakes.annotators.sections import SectionAnnotator

annotator = SectionAnnotator()
doc = annotator.process(doc)

for section in doc.sections:
    print(f"Section: {section.section_type} ({section.start}-{section.end})")
```

### NERAnnotator

Performs Named Entity Recognition for clinical entities.

**Entity Types:**
- MEDICATION
- DOSAGE  
- FREQUENCY
- CONDITION
- SYMPTOM
- ANATOMY
- PROCEDURE
- TEST_RESULT

**Approaches:**
- **Rule-based**: Pattern matching with clinical dictionaries
- **Model-based**: Using pre-trained clinical NLP models

**Configuration:**
```json
{
  "ner": {
    "approach": "rule_based",  // or "model_based"
    "model_name": "clinical_ner_model",
    "custom_patterns": {
      "MEDICATION": ["aspirin", "ibuprofen", "metformin"]
    }
  }
}
```

**Usage:**
```python
from pyctakes.annotators.ner import NERAnnotator

annotator = NERAnnotator(approach="rule_based")
doc = annotator.process(doc)

for entity in doc.entities:
    print(f"Entity: {entity.text} ({entity.label}) at {entity.start}-{entity.end}")
```

### AssertionAnnotator

Detects negation, uncertainty, and other assertion attributes.

**Assertion Types:**
- **Polarity**: POSITIVE, NEGATIVE
- **Uncertainty**: CERTAIN, UNCERTAIN  
- **Temporality**: PRESENT, PAST, FUTURE
- **Experiencer**: PATIENT, FAMILY, OTHER

**Algorithm**: Based on pyConText with clinical-specific rules.

**Configuration:**
```json
{
  "assertion": {
    "window_size": 10,
    "custom_negation_terms": ["denies", "negative for"],
    "custom_uncertainty_terms": ["possible", "maybe"]
  }
}
```

**Usage:**
```python
from pyctakes.annotators.assertion import AssertionAnnotator

annotator = AssertionAnnotator()
doc = annotator.process(doc)

for entity in doc.entities:
    assertion = entity.assertion
    print(f"{entity.text}: polarity={assertion.polarity}, "
          f"uncertainty={assertion.uncertainty}")
```

### UMLSAnnotator

Maps clinical concepts to UMLS (Unified Medical Language System) codes.

**Features:**
- Concept normalization
- CUI (Concept Unique Identifier) assignment
- Semantic type mapping
- Approximate string matching

**Configuration:**
```json
{
  "umls": {
    "similarity_threshold": 0.8,
    "max_candidates": 5,
    "semantic_types": ["T047", "T184"]  // Diseases, Signs/Symptoms
  }
}
```

**Usage:**
```python
from pyctakes.annotators.umls import UMLSAnnotator

annotator = UMLSAnnotator()
doc = annotator.process(doc)

for entity in doc.entities:
    if entity.umls_concept:
        print(f"{entity.text} -> {entity.umls_concept.cui} ({entity.umls_concept.preferred_term})")
```

## Annotation Lifecycle

1. **Text Input**: Raw clinical text
2. **Tokenization**: Sentence segmentation and tokenization
3. **Section Detection**: Identify document structure
4. **Named Entity Recognition**: Extract clinical entities
5. **Assertion Detection**: Determine entity attributes
6. **Concept Mapping**: Map to standard vocabularies

## Custom Annotators

You can create custom annotators by extending the base annotator class:

```python
from pyctakes.annotators.base import BaseAnnotator
from pyctakes.types import Document, Annotation

class CustomAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        # Initialize your annotator
    
    def process(self, doc: Document) -> Document:
        # Your processing logic
        annotation = Annotation(
            start=0,
            end=10,
            text="example",
            label="CUSTOM"
        )
        doc.annotations.append(annotation)
        return doc
```

## Performance Considerations

- **Tokenization**: spaCy backend is fastest, Stanza most accurate
- **NER**: Rule-based is faster, model-based more accurate
- **UMLS**: Enable caching for repeated concept lookups
- **Pipeline Order**: Tokenization → Sections → NER → Assertion → UMLS

## Error Handling

All annotators include robust error handling:

```python
try:
    doc = annotator.process(doc)
except AnnotationError as e:
    print(f"Annotation failed: {e}")
    # Handle gracefully
```

## Best Practices

1. **Configure appropriately**: Adjust parameters for your use case
2. **Process in order**: Follow the recommended pipeline sequence
3. **Validate outputs**: Check annotation quality on sample data
4. **Monitor performance**: Profile for bottlenecks in production
5. **Handle errors**: Implement robust error handling
