# Examples

This page provides comprehensive examples of using PyCTAKES for various clinical NLP tasks.

## Basic Examples

### Simple Entity Extraction

```python
import pyctakes

# Create a basic pipeline
pipeline = pyctakes.create_basic_pipeline()

# Process clinical text
text = "Patient has diabetes and takes metformin 500mg twice daily."
result = pipeline.process_text(text)

# Extract entities
entities = result.document.get_annotations("NAMED_ENTITY")
for entity in entities:
    print(f"{entity.text} ({entity.entity_type.value})")
```

Output:
```
diabetes (disorder)
metformin (medication)
```

### Processing with Negation Detection

```python
import pyctakes
from pyctakes.types import AnnotationType

# Use default pipeline with assertion detection
pipeline = pyctakes.create_default_pipeline()

text = """
Patient denies chest pain and shortness of breath.
No history of diabetes or hypertension.
Currently taking aspirin daily.
"""

result = pipeline.process_text(text)

# Show entities with assertion status
entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
for entity in entities:
    assertion = getattr(entity, 'assertion', 'PRESENT')
    print(f"{entity.text:20} | {entity.entity_type.value:12} | {assertion}")
```

Output:
```
chest pain           | disorder     | NEGATED
shortness of breath  | sign_symptom | NEGATED
diabetes             | disorder     | NEGATED
hypertension         | disorder     | NEGATED
aspirin              | medication   | PRESENT
```

## Clinical Note Processing

### Complete Clinical Note

```python
import pyctakes
from pyctakes.types import AnnotationType

# Sample clinical note
clinical_note = """
CHIEF COMPLAINT: Chest pain

HISTORY OF PRESENT ILLNESS:
67-year-old male with history of CAD and diabetes presents with acute chest pain.
Patient denies shortness of breath or nausea.

MEDICATIONS:
1. Metformin 1000mg BID
2. Lisinopril 10mg daily
3. Aspirin 81mg daily

ASSESSMENT:
Likely angina. Continue current medications.
"""

# Process with default pipeline
pipeline = pyctakes.create_default_pipeline()
result = pipeline.process_text(clinical_note, doc_id="note_001")

print(f"Document: {result.document.doc_id}")
print(f"Processing time: {result.processing_time:.3f}s")
print(f"Total annotations: {len(result.document.annotations)}")

# Analyze by annotation type
sentences = result.document.get_annotations(AnnotationType.SENTENCE)
sections = result.document.get_annotations(AnnotationType.SECTION)
entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)

print(f"\nBreakdown:")
print(f"  Sentences: {len(sentences)}")
print(f"  Sections: {len(sections)}")
print(f"  Entities: {len(entities)}")

# Show clinical sections
print(f"\nClinical Sections:")
for section in sections:
    print(f"  {section.section_type}: {section.text[:50]}...")
```

### Medication Extraction

```python
import pyctakes
from pyctakes.types import EntityType, AnnotationType

def extract_medications(text):
    """Extract medications with dosages and frequencies."""
    
    pipeline = pyctakes.create_default_pipeline()
    result = pipeline.process_text(text)
    
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    medications = [e for e in entities if e.entity_type == EntityType.MEDICATION]
    
    return medications

# Example medication list
med_text = """
MEDICATIONS:
1. Metformin 1000mg twice daily for diabetes
2. Lisinopril 10mg once daily for hypertension  
3. Atorvastatin 40mg at bedtime for hyperlipidemia
4. Aspirin 81mg daily for cardioprotection
5. Albuterol inhaler PRN for asthma
"""

medications = extract_medications(med_text)

print("Extracted Medications:")
for med in medications:
    print(f"  - {med.text} (confidence: {med.confidence:.2f})")
```

## Advanced Examples

### Custom Pipeline Configuration

```python
import pyctakes
from pyctakes.annotators import (
    ClinicalTokenizer, 
    ClinicalNERAnnotator, 
    NegationAssertionAnnotator
)

# Create custom configuration
config = {
    "tokenizer": {
        "backend": "spacy",
        "include_pos": True,
        "include_lemma": True
    },
    "ner": {
        "use_model": False,  # Rules only
        "use_rules": True
    },
    "assertion": {
        "max_scope": 8,
        "custom_cues": [
            {
                "literal": "patient reports no",
                "category": "negation",
                "direction": "forward",
                "max_distance": 5
            }
        ]
    }
}

# Build custom pipeline
from pyctakes import Pipeline

pipeline = Pipeline()
pipeline.add_annotator(ClinicalTokenizer(config.get("tokenizer", {})))
pipeline.add_annotator(ClinicalNERAnnotator(config.get("ner", {})))
pipeline.add_annotator(NegationAssertionAnnotator(config.get("assertion", {})))

# Test custom pipeline
text = "Patient reports no chest pain or shortness of breath."
result = pipeline.process_text(text)

entities = result.document.get_annotations("NAMED_ENTITY")
for entity in entities:
    assertion = getattr(entity, 'assertion', 'PRESENT')
    print(f"{entity.text} -> {assertion}")
```

### Batch Processing

```python
import pyctakes
from pathlib import Path
import json

def process_clinical_notes_batch(notes_directory, output_directory):
    """Process multiple clinical notes and save results."""
    
    # Create pipeline once for efficiency
    pipeline = pyctakes.create_default_pipeline()
    
    notes_dir = Path(notes_directory)
    output_dir = Path(output_directory)
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for note_file in notes_dir.glob("*.txt"):
        print(f"Processing {note_file.name}...")
        
        # Read and process note
        text = note_file.read_text()
        result = pipeline.process_text(text, doc_id=note_file.stem)
        
        # Extract key information
        entities = result.document.get_annotations("NAMED_ENTITY")
        sections = result.document.get_annotations("SECTION")
        
        # Save results
        output_data = {
            "document_id": result.document.doc_id,
            "processing_time": result.processing_time,
            "entity_count": len(entities),
            "section_count": len(sections),
            "entities": [
                {
                    "text": e.text,
                    "type": e.entity_type.value,
                    "start": e.start,
                    "end": e.end,
                    "confidence": e.confidence
                }
                for e in entities
            ],
            "sections": [
                {
                    "type": s.section_type,
                    "start": s.start,
                    "end": s.end
                }
                for s in sections
            ]
        }
        
        # Save individual result
        output_file = output_dir / f"{note_file.stem}_annotations.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        results.append(output_data)
    
    # Save summary
    summary = {
        "total_documents": len(results),
        "total_entities": sum(r["entity_count"] for r in results),
        "total_sections": sum(r["section_count"] for r in results),
        "average_processing_time": sum(r["processing_time"] for r in results) / len(results)
    }
    
    with open(output_dir / "batch_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    return results

# Usage
# results = process_clinical_notes_batch("./clinical_notes", "./annotations")
```

### Performance Comparison

```python
import pyctakes
import time

def compare_pipeline_performance(text):
    """Compare performance of different pipeline types."""
    
    pipelines = {
        "Basic": pyctakes.create_basic_pipeline(),
        "Fast": pyctakes.create_fast_pipeline(),
        "Default": pyctakes.create_default_pipeline()
    }
    
    results = {}
    
    for name, pipeline in pipelines.items():
        # Warm up
        pipeline.process_text("test")
        
        # Time multiple runs
        times = []
        for _ in range(5):
            start = time.time()
            result = pipeline.process_text(text)
            end = time.time()
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        
        results[name] = {
            "avg_time": avg_time,
            "annotations": len(result.document.annotations),
            "entities": len(result.document.get_annotations("NAMED_ENTITY"))
        }
    
    return results

# Test with sample text
sample_text = """
Patient is a 67-year-old male with diabetes, hypertension, and CAD.
Current medications include metformin, lisinopril, and aspirin.
Patient denies chest pain but reports fatigue.
"""

performance = compare_pipeline_performance(sample_text)

print("Pipeline Performance Comparison:")
print(f"{'Pipeline':<10} {'Time (s)':<10} {'Total Ann.':<12} {'Entities':<10}")
print("-" * 50)

for name, stats in performance.items():
    print(f"{name:<10} {stats['avg_time']:<10.3f} {stats['annotations']:<12} {stats['entities']:<10}")
```

## Clinical Use Cases

### Phenotyping Example

```python
import pyctakes
from collections import defaultdict

def phenotype_patients(clinical_notes):
    """Identify patients with specific conditions."""
    
    pipeline = pyctakes.create_default_pipeline()
    
    # Define phenotype criteria
    diabetes_terms = {"diabetes", "diabetes mellitus", "dm", "diabetic"}
    hypertension_terms = {"hypertension", "htn", "high blood pressure"}
    cad_terms = {"coronary artery disease", "cad", "coronary disease"}
    
    patient_phenotypes = defaultdict(set)
    
    for patient_id, note_text in clinical_notes.items():
        result = pipeline.process_text(note_text, doc_id=patient_id)
        
        entities = result.document.get_annotations("NAMED_ENTITY")
        
        # Check for conditions (only non-negated)
        for entity in entities:
            if hasattr(entity, 'assertion') and entity.assertion and 'NEGATED' in entity.assertion.value:
                continue  # Skip negated entities
                
            entity_text = entity.text.lower()
            
            if any(term in entity_text for term in diabetes_terms):
                patient_phenotypes[patient_id].add("diabetes")
            
            if any(term in entity_text for term in hypertension_terms):
                patient_phenotypes[patient_id].add("hypertension")
            
            if any(term in entity_text for term in cad_terms):
                patient_phenotypes[patient_id].add("cad")
    
    return dict(patient_phenotypes)

# Example usage
sample_notes = {
    "patient_001": "67-year-old male with diabetes and hypertension. No CAD.",
    "patient_002": "45-year-old female with coronary artery disease. Denies diabetes.",
    "patient_003": "Patient has diabetes mellitus and takes metformin."
}

phenotypes = phenotype_patients(sample_notes)

print("Patient Phenotypes:")
for patient_id, conditions in phenotypes.items():
    print(f"  {patient_id}: {', '.join(conditions) if conditions else 'No conditions found'}")
```

### Quality Metrics Extraction

```python
import pyctakes
import re

def extract_quality_metrics(clinical_text):
    """Extract quality metrics from clinical notes."""
    
    pipeline = pyctakes.create_default_pipeline()
    result = pipeline.process_text(clinical_text)
    
    metrics = {}
    
    # Extract vital signs using patterns
    text = result.document.text
    
    # Blood pressure
    bp_pattern = r'(?:bp|blood pressure)\s*:?\s*(\d{2,3})/(\d{2,3})'
    bp_match = re.search(bp_pattern, text, re.IGNORECASE)
    if bp_match:
        metrics['systolic_bp'] = int(bp_match.group(1))
        metrics['diastolic_bp'] = int(bp_match.group(2))
    
    # Heart rate
    hr_pattern = r'(?:hr|heart rate)\s*:?\s*(\d{2,3})'
    hr_match = re.search(hr_pattern, text, re.IGNORECASE)
    if hr_match:
        metrics['heart_rate'] = int(hr_match.group(1))
    
    # HbA1c
    a1c_pattern = r'(?:hba1c|a1c)\s*:?\s*(\d{1,2}\.?\d?)'
    a1c_match = re.search(a1c_pattern, text, re.IGNORECASE)
    if a1c_match:
        metrics['hba1c'] = float(a1c_match.group(1))
    
    # Extract medications for adherence
    entities = result.document.get_annotations("NAMED_ENTITY")
    medications = [e.text for e in entities if e.entity_type.value == "medication"]
    metrics['medications'] = medications
    
    # Check for medication adherence language
    adherence_positive = ["compliant", "adherent", "taking as prescribed"]
    adherence_negative = ["non-compliant", "not taking", "missed doses"]
    
    text_lower = text.lower()
    if any(phrase in text_lower for phrase in adherence_positive):
        metrics['medication_adherence'] = "good"
    elif any(phrase in text_lower for phrase in adherence_negative):
        metrics['medication_adherence'] = "poor"
    
    return metrics

# Example
quality_text = """
VITAL SIGNS: BP 145/92, HR 78, Temp 98.6F
LABS: HbA1c 7.2%
MEDICATIONS: Patient is compliant with metformin and lisinopril.
ASSESSMENT: Diabetes with suboptimal control.
"""

metrics = extract_quality_metrics(quality_text)
print("Quality Metrics:")
for key, value in metrics.items():
    print(f"  {key}: {value}")
```

## Command Line Examples

### Basic Annotation

```bash
# Create a sample clinical note
echo "Patient has diabetes and takes metformin 500mg twice daily." > sample.txt

# Annotate with default pipeline
pyctakes annotate sample.txt --output annotations.json

# View results
cat annotations.json
```

### Different Pipeline Types

```bash
# Fast pipeline for quick processing
pyctakes annotate sample.txt --pipeline fast --format text

# Basic pipeline
pyctakes annotate sample.txt --pipeline basic --output basic_results.json

# With custom configuration
pyctakes annotate sample.txt --config config.json --output configured_results.json
```

### Batch Processing

```bash
# Process multiple files
mkdir clinical_notes annotations

# Add some sample files
echo "Patient has CAD and diabetes." > clinical_notes/note1.txt
echo "67-year-old with hypertension." > clinical_notes/note2.txt

# Process all files
for file in clinical_notes/*.txt; do
    basename=$(basename "$file" .txt)
    pyctakes annotate "$file" --output "annotations/${basename}_annotations.json"
done
```

## Integration Examples

### Flask Web Application

```python
from flask import Flask, request, jsonify
import pyctakes

app = Flask(__name__)

# Initialize pipeline once
pipeline = pyctakes.create_default_pipeline()

@app.route('/annotate', methods=['POST'])
def annotate_text():
    """API endpoint for text annotation."""
    
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Process text
        result = pipeline.process_text(
            data['text'], 
            doc_id=data.get('doc_id', 'api_request')
        )
        
        # Format response
        entities = result.document.get_annotations("NAMED_ENTITY")
        
        response = {
            'document_id': result.document.doc_id,
            'processing_time': result.processing_time,
            'entities': [
                {
                    'text': e.text,
                    'type': e.entity_type.value,
                    'start': e.start,
                    'end': e.end,
                    'confidence': e.confidence
                }
                for e in entities
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Pandas Integration

```python
import pandas as pd
import pyctakes

def annotate_dataframe(df, text_column='clinical_text', id_column='patient_id'):
    """Annotate clinical text in a pandas DataFrame."""
    
    pipeline = pyctakes.create_default_pipeline()
    
    results = []
    
    for idx, row in df.iterrows():
        text = row[text_column]
        doc_id = row[id_column] if id_column in df.columns else f"doc_{idx}"
        
        result = pipeline.process_text(text, doc_id=doc_id)
        entities = result.document.get_annotations("NAMED_ENTITY")
        
        # Count entities by type
        entity_counts = {}
        for entity in entities:
            entity_type = entity.entity_type.value
            entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
        
        results.append({
            'document_id': doc_id,
            'processing_time': result.processing_time,
            'total_entities': len(entities),
            **entity_counts
        })
    
    return pd.DataFrame(results)

# Example usage
clinical_df = pd.DataFrame({
    'patient_id': ['P001', 'P002', 'P003'],
    'clinical_text': [
        'Patient has diabetes and hypertension',
        'CAD with chest pain, takes aspirin',
        'No known medical conditions'
    ]
})

annotations_df = annotate_dataframe(clinical_df)
print(annotations_df)
```

These examples demonstrate the versatility and power of PyCTAKES for various clinical NLP tasks. Start with the basic examples and gradually work your way up to more complex use cases.
