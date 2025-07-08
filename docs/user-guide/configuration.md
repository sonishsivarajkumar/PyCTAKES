# Configuration

PyTAKES provides flexible configuration options to customize the behavior of annotators and pipelines.

## Configuration File Format

PyTAKES uses JSON configuration files:

```json
{
  "tokenization": {
    "backend": "spacy",
    "model": "en_core_web_sm"
  },
  "sections": {
    "enabled": true,
    "custom_patterns": {}
  },
  "ner": {
    "approach": "rule_based",
    "custom_patterns": {}
  },
  "assertion": {
    "window_size": 10
  },
  "umls": {
    "similarity_threshold": 0.8
  }
}
```

## Annotator Configuration

### Tokenization Configuration

```json
{
  "tokenization": {
    "backend": "spacy",           // Backend: "spacy", "stanza", "rule_based"
    "model": "en_core_web_sm",    // Model name (for spacy/stanza)
    "sentence_split": true,       // Enable sentence segmentation
    "tokenize": true,             // Enable tokenization
    "preserve_whitespace": false  // Preserve original whitespace
  }
}
```

**Backend Options:**
- `spacy`: Fast, requires spaCy model installation
- `stanza`: Most accurate, requires Stanza models  
- `rule_based`: No dependencies, basic splitting

### Section Configuration

```json
{
  "sections": {
    "enabled": true,
    "case_sensitive": false,
    "custom_patterns": {
      "CHIEF_COMPLAINT": [
        "chief complaint:",
        "cc:",
        "presenting complaint"
      ],
      "CUSTOM_SECTION": [
        "my custom section:",
        "special notes:"
      ]
    },
    "disabled_sections": ["FAMILY_HISTORY"]
  }
}
```

### NER Configuration

```json
{
  "ner": {
    "approach": "rule_based",     // "rule_based" or "model_based"
    "model_name": null,           // Model for model_based approach
    "case_sensitive": false,
    "custom_patterns": {
      "MEDICATION": [
        "aspirin", "ibuprofen", "metformin",
        "lisinopril", "atorvastatin"
      ],
      "CONDITION": [
        "diabetes", "hypertension", "pneumonia"
      ]
    },
    "entity_types": [             // Limit to specific entity types
      "MEDICATION", "CONDITION", "SYMPTOM"
    ]
  }
}
```

### Assertion Configuration

```json
{
  "assertion": {
    "window_size": 10,            // Context window for assertion detection
    "custom_negation_terms": [
      "denies", "negative for", "ruled out",
      "no evidence of", "absent"
    ],
    "custom_uncertainty_terms": [
      "possible", "probable", "likely",
      "suspect", "consider"
    ],
    "custom_temporal_terms": {
      "PAST": ["history of", "previous", "prior"],
      "FUTURE": ["will", "plan to", "scheduled"]
    }
  }
}
```

### UMLS Configuration

```json
{
  "umls": {
    "similarity_threshold": 0.8,  // Minimum similarity for concept matching
    "max_candidates": 5,          // Maximum candidate concepts
    "semantic_types": [           // Filter by semantic types
      "T047",  // Disease or Syndrome
      "T184",  // Sign or Symptom
      "T121"   // Pharmacologic Substance
    ],
    "sources": [                  // Limit to specific vocabularies
      "SNOMEDCT_US", "RXNORM", "ICD10CM"
    ],
    "enable_caching": true        // Cache concept lookups
  }
}
```

## Pipeline Configuration

### Default Pipeline

```json
{
  "pipeline": {
    "name": "default",
    "annotators": [
      {
        "name": "tokenization",
        "class": "TokenizationAnnotator",
        "config": {
          "backend": "spacy"
        }
      },
      {
        "name": "sections", 
        "class": "SectionAnnotator",
        "config": {}
      },
      {
        "name": "ner",
        "class": "NERAnnotator", 
        "config": {
          "approach": "rule_based"
        }
      },
      {
        "name": "assertion",
        "class": "AssertionAnnotator",
        "config": {}
      },
      {
        "name": "umls",
        "class": "UMLSAnnotator",
        "config": {}
      }
    ]
  }
}
```

### Custom Pipeline

```json
{
  "pipeline": {
    "name": "medication_only",
    "annotators": [
      {
        "name": "tokenization",
        "class": "TokenizationAnnotator",
        "config": {
          "backend": "rule_based"
        }
      },
      {
        "name": "ner",
        "class": "NERAnnotator",
        "config": {
          "approach": "rule_based",
          "entity_types": ["MEDICATION", "DOSAGE"]
        }
      }
    ]
  }
}
```

## Environment Variables

PyTAKES recognizes these environment variables:

```bash
# UMLS API Key (required for full UMLS functionality)
export UMLS_API_KEY="your-api-key"

# spaCy model path
export SPACY_MODEL_PATH="/path/to/models"

# Cache directory
export PYTAKES_CACHE_DIR="/path/to/cache"

# Log level
export PYTAKES_LOG_LEVEL="INFO"
```

## Configuration Loading

### From File

```python
from pytakes.pipeline import Pipeline

# Load from file
pipeline = Pipeline.from_config("config.json")

# Load with overrides
pipeline = Pipeline.from_config(
    "config.json",
    overrides={"ner.approach": "model_based"}
)
```

### From Dictionary

```python
config = {
    "tokenization": {"backend": "spacy"},
    "ner": {"approach": "rule_based"}
}

pipeline = Pipeline.from_config(config)
```

### Programmatic Configuration

```python
from pytakes.pipeline import Pipeline
from pytakes.annotators import TokenizationAnnotator, NERAnnotator

pipeline = Pipeline()
pipeline.add_annotator(TokenizationAnnotator(backend="spacy"))
pipeline.add_annotator(NERAnnotator(approach="rule_based"))
```

## Configuration Validation

PyTAKES validates configuration on load:

```python
try:
    pipeline = Pipeline.from_config("config.json")
except ConfigurationError as e:
    print(f"Invalid configuration: {e}")
```

## Common Configuration Patterns

### High Performance Setup

```json
{
  "tokenization": {"backend": "rule_based"},
  "ner": {"approach": "rule_based"},
  "assertion": {"window_size": 5},
  "umls": {"similarity_threshold": 0.9}
}
```

### High Accuracy Setup

```json
{
  "tokenization": {"backend": "stanza"},
  "ner": {"approach": "model_based"},
  "assertion": {"window_size": 15},
  "umls": {"similarity_threshold": 0.7}
}
```

### Medication-Focused Pipeline

```json
{
  "ner": {
    "entity_types": ["MEDICATION", "DOSAGE", "FREQUENCY"],
    "custom_patterns": {
      "MEDICATION": ["list", "of", "medications"]
    }
  },
  "umls": {
    "semantic_types": ["T121"],  // Pharmacologic Substance
    "sources": ["RXNORM"]
  }
}
```

## Best Practices

1. **Start Simple**: Begin with default configuration
2. **Validate Early**: Test configuration on sample data
3. **Monitor Performance**: Profile with different settings
4. **Version Control**: Store configurations in version control
5. **Document Changes**: Keep notes on configuration rationale
6. **Test Thoroughly**: Validate changes don't break existing functionality
