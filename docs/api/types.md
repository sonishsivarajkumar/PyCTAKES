# Types API Reference

PyCTAKES uses a comprehensive type system to represent clinical text and annotations.

## Core Types

### `class Document`

Main document class containing text and all annotations.

**Attributes:**
- `text` (str): The clinical text content
- `metadata` (dict): Document metadata
- `sentences` (List[Sentence]): Sentence annotations
- `tokens` (List[Token]): Token annotations
- `entities` (List[Entity]): Entity annotations
- `sections` (List[Section]): Section annotations
- `annotations` (List[Annotation]): All annotations

**Methods:**
- `to_json()`: Serialize to JSON
- `from_json(data)`: Deserialize from JSON

### `class Annotation`

Base class for all annotations.

**Attributes:**
- `start` (int): Start character position
- `end` (int): End character position
- `text` (str): Annotated text span
- `label` (str): Annotation label/type
- `confidence` (float): Confidence score (0.0-1.0)

### `class Token(Annotation)`

Represents a single token.

**Attributes:**
- `pos` (str): Part-of-speech tag
- `lemma` (str): Lemmatized form
- `is_alpha` (bool): Contains alphabetic characters
- `is_digit` (bool): Contains only digits
- `is_punct` (bool): Is punctuation

### `class Sentence(Annotation)`

Represents a sentence with tokens.

**Attributes:**
- `tokens` (List[Token]): Tokens in the sentence

### `class Entity(Annotation)`

Represents a named entity.

**Attributes:**
- `assertion` (Assertion): Assertion information
- `umls_concept` (UMLSConcept): UMLS concept mapping

### `class Section(Annotation)`

Represents a document section.

**Attributes:**
- `section_type` (str): Type of section

### `class Assertion`

Assertion attributes for entities.

**Attributes:**
- `polarity` (str): POSITIVE, NEGATIVE
- `uncertainty` (str): CERTAIN, UNCERTAIN
- `temporality` (str): PRESENT, PAST, FUTURE
- `experiencer` (str): PATIENT, FAMILY, OTHER

### `class UMLSConcept`

UMLS concept information.

**Attributes:**
- `cui` (str): Concept Unique Identifier
- `preferred_term` (str): Preferred term
- `semantic_types` (List[str]): Semantic type codes
- `sources` (List[str]): Source vocabularies
- `confidence` (float): Mapping confidence

## Usage Examples

### Creating Documents

```python
from pyctakes.types import Document

# Create document from text
doc = Document(text="Patient has diabetes and hypertension.")

# Create with metadata
doc = Document(
    text="Clinical note text",
    metadata={
        "patient_id": "12345",
        "note_type": "progress_note",
        "date": "2025-01-15"
    }
)
```

### Working with Annotations

```python
from pyctakes.types import Annotation, Document

doc = Document(text="Patient has diabetes.")

# Create annotation
annotation = Annotation(
    start=12,
    end=20,
    text="diabetes",
    label="CONDITION",
    confidence=0.95
)

# Add to document
doc.annotations.append(annotation)

# Access annotations
for ann in doc.annotations:
    print(f"{ann.text}: {ann.label} ({ann.confidence})")
```

### Working with Entities

```python
from pyctakes.types import Entity, Assertion

# Create entity with assertion
entity = Entity(
    start=12,
    end=20,
    text="diabetes",
    label="CONDITION",
    assertion=Assertion(
        polarity="POSITIVE",
        uncertainty="CERTAIN",
        temporality="PRESENT"
    )
)

# Add to document
doc.entities.append(entity)
```

### Working with Tokens

```python
from pyctakes.types import Token, Sentence

# Create tokens
tokens = [
    Token(start=0, end=7, text="Patient", pos="NOUN"),
    Token(start=8, end=11, text="has", pos="VERB"),
    Token(start=12, end=20, text="diabetes", pos="NOUN")
]

# Create sentence
sentence = Sentence(
    start=0,
    end=21,
    text="Patient has diabetes.",
    tokens=tokens
)

# Add to document
doc.sentences.append(sentence)
```

### Working with Sections

```python
from pyctakes.types import Section

# Create section
section = Section(
    start=0,
    end=100,
    section_type="CHIEF_COMPLAINT",
    text="Chief Complaint: Chest pain for 2 days."
)

# Add to document
doc.sections.append(section)
```

### Working with UMLS Concepts

```python
from pyctakes.types import UMLSConcept

# Create UMLS concept
concept = UMLSConcept(
    cui="C0011849",
    preferred_term="Diabetes Mellitus",
    semantic_types=["T047"],  # Disease or Syndrome
    sources=["SNOMEDCT_US", "ICD10CM"],
    confidence=0.89
)

# Attach to entity
entity.umls_concept = concept
```

## Type Hierarchies

### Annotation Hierarchy

```
Annotation (base)
├── Token
├── Sentence  
├── Entity
└── Section
```

### Entity Types

Common entity labels used in PyCTAKES:

- **MEDICATION**: Drugs and medications
- **DOSAGE**: Medication dosages
- **FREQUENCY**: Dosing frequency
- **CONDITION**: Medical conditions and diseases
- **SYMPTOM**: Signs and symptoms
- **ANATOMY**: Anatomical structures
- **PROCEDURE**: Medical procedures
- **TEST_RESULT**: Lab results and measurements

### Section Types

Standard clinical section types:

- **CHIEF_COMPLAINT**: Primary reason for visit
- **HISTORY_OF_PRESENT_ILLNESS**: Current problem details
- **PAST_MEDICAL_HISTORY**: Previous medical history
- **MEDICATIONS**: Current medications
- **ALLERGIES**: Known allergies
- **SOCIAL_HISTORY**: Social and lifestyle factors
- **FAMILY_HISTORY**: Family medical history
- **REVIEW_OF_SYSTEMS**: Systematic review
- **PHYSICAL_EXAMINATION**: Physical exam findings
- **ASSESSMENT_AND_PLAN**: Clinical assessment and treatment plan

### Assertion Values

#### Polarity
- **POSITIVE**: Entity is present/affirmed
- **NEGATIVE**: Entity is negated/denied

#### Uncertainty
- **CERTAIN**: Definite statement
- **UNCERTAIN**: Possible/probable/likely

#### Temporality
- **PRESENT**: Current condition
- **PAST**: Historical condition
- **FUTURE**: Future/planned condition

#### Experiencer
- **PATIENT**: Refers to the patient
- **FAMILY**: Refers to family member
- **OTHER**: Refers to someone else

## JSON Serialization

All types support JSON serialization:

```python
import json
from pyctakes.types import Document

# Create document with annotations
doc = Document(text="Patient has diabetes.")
# ... add annotations ...

# Serialize to JSON
json_data = doc.to_json()
print(json.dumps(json_data, indent=2))

# Deserialize from JSON
doc_restored = Document.from_json(json_data)
```

Example JSON output:
```json
{
  "text": "Patient has diabetes.",
  "metadata": {},
  "sentences": [
    {
      "start": 0,
      "end": 21,
      "text": "Patient has diabetes.",
      "tokens": [
        {
          "start": 0,
          "end": 7,
          "text": "Patient",
          "pos": "NOUN",
          "lemma": "patient"
        }
      ]
    }
  ],
  "entities": [
    {
      "start": 12,
      "end": 20,
      "text": "diabetes",
      "label": "CONDITION",
      "confidence": 0.95,
      "assertion": {
        "polarity": "POSITIVE",
        "uncertainty": "CERTAIN",
        "temporality": "PRESENT",
        "experiencer": "PATIENT"
      }
    }
  ],
  "sections": [
    {
      "start": 0,
      "end": 21,
      "section_type": "ASSESSMENT_AND_PLAN"
    }
  ]
}
```

## Type Validation

PyCTAKES includes validation for type safety:

```python
from pyctakes.types import Document, ValidationError

try:
    # Invalid annotation (end before start)
    annotation = Annotation(start=10, end=5, text="invalid")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Extending Types

You can extend the base types for custom use cases:

```python
from pyctakes.types import Entity
from dataclasses import dataclass

@dataclass
class CustomEntity(Entity):
    custom_field: str = ""
    custom_score: float = 0.0
    
    def custom_method(self):
        return f"Custom: {self.text}"
```

## Best Practices

1. **Use appropriate types**: Choose the most specific type for your annotations
2. **Set confidence scores**: Always provide confidence when available
3. **Validate inputs**: Check spans and text alignment
4. **Use standard labels**: Stick to established entity and section types
5. **Include metadata**: Add relevant document metadata for tracking
