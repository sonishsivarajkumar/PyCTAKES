# UMLS Integration

Comprehensive guide to integrating pyCTAKES with the Unified Medical Language System (UMLS).

## Overview

The Unified Medical Language System (UMLS) is a comprehensive set of files and software that brings together biomedical vocabularies and standards to enable interoperability between systems. pyCTAKES provides flexible UMLS integration for concept normalization and mapping.

## UMLS Components

### Key Vocabularies

- **SNOMED CT**: Systematic clinical terminology
- **RxNorm**: Normalized drug names
- **LOINC**: Laboratory data
- **ICD-10-CM**: International disease classification
- **CPT**: Current procedural terminology
- **MeSH**: Medical subject headings

### UMLS Identifiers

- **CUI**: Concept Unique Identifier (primary key)
- **AUI**: Atom Unique Identifier (term variants)
- **SUI**: String Unique Identifier (unique strings)

## Setup and Configuration

### UMLS License and Access

1. **Obtain UMLS License**: Register at [UTS](https://uts.nlm.nih.gov/)
2. **Download UMLS**: Get the current release
3. **Generate API Key**: Create API key for programmatic access

### Installation Options

#### Option 1: QuickUMLS (Recommended)

```bash
# Install QuickUMLS
pip install quickumls

# Download and install UMLS
python -m quickumls.install /path/to/umls/installation \
    --destination /path/to/quickumls/data
```

#### Option 2: UMLS REST API

```python
# Use UMLS REST API (requires API key)
import requests

class UMLSClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://uts-ws.nlm.nih.gov/rest"
    
    def search_concept(self, term):
        # Implementation for REST API calls
        pass
```

#### Option 3: Local Dictionary

```python
# Use simplified local dictionary for development
umls_dict = {
    "diabetes": {
        "cui": "C0011849",
        "preferred_term": "Diabetes Mellitus",
        "semantic_types": ["T047"]
    }
}
```

## pyCTAKES UMLS Integration

### Basic UMLS Annotator

```python
from pyctakes.annotators.umls import UMLSConceptMapper

# Create UMLS annotator
umls = UMLSConceptMapper(
    umls_path="/path/to/quickumls/data",
    similarity_threshold=0.8,
    max_candidates=5
)

# Add to pipeline
pipeline.add_annotator(umls)

# Process text
doc = pipeline.process_text("Patient has diabetes and hypertension.")

# Access UMLS concepts
for entity in doc.entities:
    if entity.umls_concept:
        concept = entity.umls_concept
        print(f"{entity.text} -> {concept.cui} ({concept.preferred_term})")
```

### Configuration Options

```python
umls_config = {
    "umls": {
        "enabled": True,
        "umls_path": "/path/to/quickumls/data",
        "similarity_threshold": 0.8,      # Minimum similarity score
        "max_candidates": 5,              # Maximum candidates per term
        "semantic_types": [               # Filter by semantic types
            "T047",  # Disease or Syndrome
            "T184",  # Sign or Symptom
            "T121"   # Pharmacologic Substance
        ],
        "sources": [                      # Filter by vocabulary sources
            "SNOMEDCT_US", "RXNORM", "ICD10CM"
        ],
        "overlaps": "length",             # Handle overlapping matches
        "threshold": 0.8,                 # QuickUMLS threshold
        "window": 5,                      # Context window size
        "similarity_name": "jaccard",     # Similarity function
        "accepted_semtypes": None,        # Semantic type filter
        "enable_caching": True,           # Enable result caching
        "cache_size": 10000              # Cache size limit
    }
}
```

### Advanced UMLS Annotator

```python
from pyctakes.annotators.umls import AdvancedUMLSAnnotator
from pyctakes.types import UMLSConcept

class AdvancedUMLSAnnotator(BaseAnnotator):
    def __init__(self, umls_path, **kwargs):
        super().__init__()
        
        # Initialize QuickUMLS
        from quickumls import QuickUMLS
        self.matcher = QuickUMLS(
            umls_path,
            overlapping_criteria="length",
            threshold=kwargs.get("threshold", 0.8),
            similarity_name=kwargs.get("similarity", "jaccard"),
            window=kwargs.get("window", 5)
        )
        
        self.config = kwargs
        self.cache = {}
    
    def process(self, doc: Document) -> Document:
        # Process each entity
        for entity in doc.entities:
            concepts = self._map_entity_to_umls(entity)
            if concepts:
                # Select best concept
                entity.umls_concept = self._select_best_concept(concepts)
        
        return doc
    
    def _map_entity_to_umls(self, entity):
        """Map entity text to UMLS concepts."""
        
        # Check cache first
        cache_key = entity.text.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Query QuickUMLS
        matches = self.matcher.match(entity.text)
        
        concepts = []
        for match in matches:
            for candidate in match:
                concept = UMLSConcept(
                    cui=candidate['cui'],
                    preferred_term=candidate['preferred'],
                    semantic_types=candidate['semtypes'],
                    sources=candidate.get('sources', []),
                    confidence=candidate['similarity']
                )
                concepts.append(concept)
        
        # Filter by configuration
        concepts = self._filter_concepts(concepts)
        
        # Cache results
        self.cache[cache_key] = concepts
        
        return concepts
    
    def _filter_concepts(self, concepts):
        """Filter concepts by configuration."""
        
        filtered = []
        
        for concept in concepts:
            # Filter by confidence
            if concept.confidence < self.config.get("similarity_threshold", 0.8):
                continue
            
            # Filter by semantic types
            if "semantic_types" in self.config:
                if not any(st in concept.semantic_types 
                          for st in self.config["semantic_types"]):
                    continue
            
            # Filter by sources
            if "sources" in self.config:
                if not any(src in concept.sources 
                          for src in self.config["sources"]):
                    continue
            
            filtered.append(concept)
        
        return filtered[:self.config.get("max_candidates", 5)]
    
    def _select_best_concept(self, concepts):
        """Select the best concept from candidates."""
        
        if not concepts:
            return None
        
        # Sort by confidence and return best
        concepts.sort(key=lambda x: x.confidence, reverse=True)
        return concepts[0]
```

## Semantic Types

### Common Semantic Types in Clinical NLP

```python
CLINICAL_SEMANTIC_TYPES = {
    # Disorders
    "T047": "Disease or Syndrome",
    "T048": "Mental or Behavioral Dysfunction", 
    "T191": "Neoplastic Process",
    "T046": "Pathologic Function",
    
    # Signs and Symptoms
    "T184": "Sign or Symptom",
    "T033": "Finding",
    
    # Anatomy
    "T017": "Anatomical Structure",
    "T029": "Body Location or Region",
    "T023": "Body Part, Organ, or Organ Component",
    
    # Procedures
    "T060": "Diagnostic Procedure",
    "T061": "Therapeutic or Preventive Procedure",
    "T059": "Laboratory Procedure",
    
    # Substances
    "T121": "Pharmacologic Substance",
    "T200": "Clinical Drug",
    "T103": "Chemical",
    
    # Organizations
    "T093": "Health Care Related Organization",
    "T073": "Manufactured Object"
}

# Filter by clinical semantic types
clinical_filter = list(CLINICAL_SEMANTIC_TYPES.keys())
```

### Semantic Type Filtering

```python
def filter_by_semantic_types(concepts, allowed_types):
    """Filter concepts by semantic types."""
    
    filtered = []
    for concept in concepts:
        if any(st in concept.semantic_types for st in allowed_types):
            filtered.append(concept)
    
    return filtered

# Usage
medication_types = ["T121", "T200"]  # Pharmacologic substances and drugs
med_concepts = filter_by_semantic_types(concepts, medication_types)
```

## Entity-Specific UMLS Mapping

### Medication Mapping

```python
class MedicationUMLSMapper(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        
        # Focus on RxNorm for medications
        self.umls = UMLSConceptMapper(
            sources=["RXNORM"],
            semantic_types=["T121", "T200"],  # Pharmacologic substances
            similarity_threshold=0.85
        )
    
    def process(self, doc: Document) -> Document:
        # Only process medication entities
        med_entities = [e for e in doc.entities if e.label == "MEDICATION"]
        
        for entity in med_entities:
            # Map to RxNorm concepts
            concepts = self.umls.map_entity(entity)
            if concepts:
                entity.umls_concept = concepts[0]
                
                # Add RxNorm-specific information
                entity.rxnorm_cui = concepts[0].cui
                entity.generic_name = self._get_generic_name(concepts[0])
        
        return doc
```

### Condition Mapping

```python
class ConditionUMLSMapper(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        
        # Focus on SNOMED CT for conditions
        self.umls = UMLSConceptMapper(
            sources=["SNOMEDCT_US"],
            semantic_types=["T047", "T048", "T191"],  # Diseases and disorders
            similarity_threshold=0.8
        )
    
    def process(self, doc: Document) -> Document:
        condition_entities = [e for e in doc.entities 
                            if e.label in ["CONDITION", "DISORDER"]]
        
        for entity in condition_entities:
            concepts = self.umls.map_entity(entity)
            if concepts:
                entity.umls_concept = concepts[0]
                
                # Add SNOMED-specific information
                entity.snomed_code = concepts[0].cui
                entity.icd10_codes = self._get_icd10_mappings(concepts[0])
        
        return doc
```

## Performance Optimization

### Caching Strategies

```python
from functools import lru_cache
import pickle

class CachedUMLSMapper:
    def __init__(self, cache_file="umls_cache.pkl"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        try:
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    @lru_cache(maxsize=10000)
    def map_term(self, term):
        """Map term to UMLS with caching."""
        
        if term in self.cache:
            return self.cache[term]
        
        # Perform UMLS lookup
        concepts = self._umls_lookup(term)
        
        # Cache result
        self.cache[term] = concepts
        
        return concepts
```

### Batch Processing

```python
def process_entities_batch(entities, batch_size=100):
    """Process entities in batches for better performance."""
    
    results = []
    
    for i in range(0, len(entities), batch_size):
        batch = entities[i:i + batch_size]
        
        # Extract unique terms
        unique_terms = list(set(e.text.lower() for e in batch))
        
        # Batch lookup
        term_concepts = {}
        for term in unique_terms:
            term_concepts[term] = umls_mapper.map_term(term)
        
        # Assign concepts to entities
        for entity in batch:
            concepts = term_concepts.get(entity.text.lower(), [])
            if concepts:
                entity.umls_concept = concepts[0]
        
        results.extend(batch)
    
    return results
```

## Custom UMLS Integration

### Local UMLS Dictionary

```python
class LocalUMLSMapper(BaseAnnotator):
    def __init__(self, dictionary_path):
        super().__init__()
        self.concepts = self._load_dictionary(dictionary_path)
    
    def _load_dictionary(self, path):
        """Load local UMLS dictionary."""
        
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Build efficient lookup structure
        lookup = {}
        for cui, concept_data in data.items():
            terms = concept_data.get('terms', [])
            for term in terms:
                lookup[term.lower()] = UMLSConcept(
                    cui=cui,
                    preferred_term=concept_data['preferred_term'],
                    semantic_types=concept_data['semantic_types'],
                    confidence=1.0
                )
        
        return lookup
    
    def process(self, doc: Document) -> Document:
        for entity in doc.entities:
            concept = self.concepts.get(entity.text.lower())
            if concept:
                entity.umls_concept = concept
        
        return doc
```

### REST API Integration

```python
import requests
from functools import lru_cache

class UMLSRESTMapper(BaseAnnotator):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://uts-ws.nlm.nih.gov/rest"
        self.session = requests.Session()
    
    @lru_cache(maxsize=5000)
    def _get_ticket(self):
        """Get authentication ticket."""
        
        url = f"{self.base_url}/security/ticket"
        response = self.session.post(url, data={"apikey": self.api_key})
        return response.text
    
    @lru_cache(maxsize=10000)
    def _search_concept(self, term):
        """Search for concept via REST API."""
        
        ticket = self._get_ticket()
        
        url = f"{self.base_url}/search/current"
        params = {
            "string": term,
            "ticket": ticket,
            "pageSize": 5
        }
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            concepts = []
            
            for result in data.get("result", {}).get("results", []):
                concept = UMLSConcept(
                    cui=result["ui"],
                    preferred_term=result["name"],
                    semantic_types=[],  # Would need additional API call
                    confidence=1.0
                )
                concepts.append(concept)
            
            return concepts
        
        return []
    
    def process(self, doc: Document) -> Document:
        for entity in doc.entities:
            concepts = self._search_concept(entity.text)
            if concepts:
                entity.umls_concept = concepts[0]
        
        return doc
```

## Evaluation and Quality Assurance

### Concept Mapping Evaluation

```python
def evaluate_umls_mapping(gold_standard, predictions):
    """Evaluate UMLS concept mapping quality."""
    
    correct_cuis = 0
    total_predictions = 0
    
    for gold, pred in zip(gold_standard, predictions):
        if pred.umls_concept:
            total_predictions += 1
            if pred.umls_concept.cui == gold.expected_cui:
                correct_cuis += 1
    
    precision = correct_cuis / total_predictions if total_predictions > 0 else 0
    recall = correct_cuis / len(gold_standard)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "total_mapped": total_predictions,
        "total_gold": len(gold_standard)
    }
```

### Concept Validation

```python
def validate_umls_concepts(entities):
    """Validate UMLS concept assignments."""
    
    validation_results = []
    
    for entity in entities:
        if entity.umls_concept:
            concept = entity.umls_concept
            
            # Check CUI format
            cui_valid = bool(re.match(r'^C\d{7}$', concept.cui))
            
            # Check semantic type validity
            semtype_valid = all(
                st.startswith('T') and len(st) == 4 
                for st in concept.semantic_types
            )
            
            # Check confidence range
            confidence_valid = 0.0 <= concept.confidence <= 1.0
            
            validation_results.append({
                "entity": entity.text,
                "cui": concept.cui,
                "cui_valid": cui_valid,
                "semtype_valid": semtype_valid,
                "confidence_valid": confidence_valid,
                "overall_valid": cui_valid and semtype_valid and confidence_valid
            })
    
    return validation_results
```

## Best Practices

### 1. Choose Appropriate Vocabularies
- **Medications**: Use RxNorm
- **Conditions**: Use SNOMED CT
- **Lab Tests**: Use LOINC  
- **Procedures**: Use CPT/SNOMED CT

### 2. Optimize Performance
- Enable caching for repeated lookups
- Use batch processing for multiple entities
- Filter by semantic types to reduce candidates
- Set appropriate similarity thresholds

### 3. Quality Assurance
- Validate CUI formats and semantic types
- Evaluate mapping accuracy on gold standard data
- Monitor confidence scores and adjust thresholds
- Review unmapped entities regularly

### 4. Handle Edge Cases
- Implement fallback for unmapped entities
- Handle abbreviations and synonyms
- Consider context for disambiguation
- Manage overlapping concept matches

### 5. Stay Updated
- Update UMLS releases regularly
- Monitor vocabulary changes
- Validate mappings after updates
- Document version dependencies
