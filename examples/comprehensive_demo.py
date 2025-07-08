"""Comprehensive example demonstrating PyTAKES clinical NLP capabilities."""

import pytakes
from pytakes.types import Document, AnnotationType


def demo_default_pipeline():
    """Demonstrate the default clinical pipeline."""
    print("=== Default Clinical Pipeline Demo ===")
    
    # Sample clinical text
    clinical_text = """
    CHIEF COMPLAINT: Chest pain
    
    HISTORY OF PRESENT ILLNESS:
    Patient is a 65-year-old male with a history of diabetes mellitus and hypertension.
    He presents with chest pain and shortness of breath that started 2 hours ago.
    Patient denies nausea or diaphoresis. No family history of heart disease.
    
    MEDICATIONS:
    - Metformin 500mg twice daily for diabetes
    - Lisinopril 10mg daily for blood pressure
    - Aspirin 81mg daily for cardioprotection
    
    ASSESSMENT AND PLAN:
    Patient has no evidence of acute coronary syndrome.
    Blood pressure is well controlled on current medications.
    Diabetes shows good control with current regimen.
    Will continue current medications and follow up in 3 months.
    """
    
    # Create default pipeline
    pipeline = pytakes.create_default_pipeline()
    
    # Process the text
    result = pipeline.process_text(clinical_text, doc_id="example_note")
    
    print(f"Processed document: {result.document.doc_id}")
    print(f"Processing time: {result.processing_time:.3f} seconds")
    print(f"Number of annotations: {len(result.document.annotations)}")
    
    # Show different types of annotations
    sentences = result.document.get_annotations(AnnotationType.SENTENCE)
    print(f"\nFound {len(sentences)} sentences")
    
    tokens = result.document.get_annotations(AnnotationType.TOKEN)
    print(f"Found {len(tokens)} tokens")
    
    sections = result.document.get_annotations(AnnotationType.SECTION)
    print(f"Found {len(sections)} sections:")
    for section in sections:
        print(f"  - {section.section_type}: {section.text[:50].replace(chr(10), ' ')}...")
    
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    print(f"\nFound {len(entities)} named entities:")
    for entity in entities[:10]:  # Show first 10
        assertion = getattr(entity, 'assertion', None)
        assertion_str = f" ({assertion.value})" if assertion else ""
        print(f"  - {entity.entity_type.value}: {entity.text} (conf: {entity.confidence:.2f}){assertion_str}")
    
    concepts = result.document.get_annotations(AnnotationType.CONCEPT)
    if concepts:
        print(f"\nFound {len(concepts)} concept mappings:")
        for concept in concepts[:5]:  # Show first 5
            cui = concept.metadata.get('cui', 'N/A')
            print(f"  - {concept.text} -> {cui}")


def demo_fast_pipeline():
    """Demonstrate the fast pipeline."""
    print("\n=== Fast Pipeline Demo ===")
    
    clinical_text = """
    Patient has diabetes and takes metformin 500mg twice daily.
    No chest pain or shortness of breath reported.
    Blood pressure is 120/80 mmHg.
    """
    
    # Create fast pipeline
    pipeline = pytakes.create_fast_pipeline()
    
    # Process the text
    result = pipeline.process_text(clinical_text, doc_id="fast_example")
    
    print(f"Fast processing time: {result.processing_time:.3f} seconds")
    print(f"Annotations: {len(result.document.annotations)}")
    
    # Show entities found by fast pipeline
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    print(f"Entities found:")
    for entity in entities:
        print(f"  - {entity.text} ({entity.entity_type.value})")


def demo_custom_pipeline():
    """Demonstrate creating a custom pipeline."""
    print("\n=== Custom Pipeline Demo ===")
    
    from pytakes import Pipeline
    from pytakes.annotators import (
        ClinicalTokenizer, ClinicalNERAnnotator, NegationAssertionAnnotator
    )
    
    # Create custom pipeline with specific configuration
    pipeline = Pipeline()
    
    # Add tokenizer
    pipeline.add_annotator(ClinicalTokenizer({
        "include_pos": True,
        "include_lemma": True
    }))
    
    # Add NER with rules only
    pipeline.add_annotator(ClinicalNERAnnotator({
        "use_rules": True, 
        "use_model": False
    }))
    
    # Add assertion detection
    pipeline.add_annotator(NegationAssertionAnnotator())
    
    clinical_text = """
    Patient reports no chest pain and denies shortness of breath.
    Takes aspirin daily but no history of heart disease.
    """
    
    result = pipeline.process_text(clinical_text, doc_id="custom_example")
    
    print(f"Custom pipeline found {len(result.document.annotations)} annotations")
    
    # Show tokens with POS tags
    tokens = result.document.get_annotations(AnnotationType.TOKEN)
    print("Tokens with POS tags:")
    for token in tokens[:15]:  # First 15 tokens
        pos = getattr(token, 'pos_tag', 'N/A')
        lemma = getattr(token, 'lemma', 'N/A')
        print(f"  {token.text} (POS: {pos}, Lemma: {lemma})")
    
    # Show entities with assertions
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    print("\nEntities with assertion status:")
    for entity in entities:
        assertion = getattr(entity, 'assertion', None)
        assertion_str = assertion.value if assertion else "PRESENT"
        print(f"  - {entity.text} -> {assertion_str}")


def demo_section_detection():
    """Demonstrate section detection capabilities."""
    print("\n=== Section Detection Demo ===")
    
    clinical_text = """
    CHIEF COMPLAINT:
    Chest pain and shortness of breath.
    
    HISTORY OF PRESENT ILLNESS:
    65-year-old male presents with acute onset chest pain.
    
    PAST MEDICAL HISTORY:
    1. Diabetes mellitus type 2
    2. Hypertension
    3. Hyperlipidemia
    
    MEDICATIONS:
    1. Metformin 500mg BID
    2. Lisinopril 10mg daily
    3. Atorvastatin 20mg daily
    
    SOCIAL HISTORY:
    Former smoker, quit 10 years ago.
    Occasional alcohol use.
    
    ASSESSMENT AND PLAN:
    Continue current medications.
    Follow up in 3 months.
    """
    
    # Use basic pipeline to focus on sections
    pipeline = pytakes.create_basic_pipeline()
    result = pipeline.process_text(clinical_text, doc_id="section_example")
    
    sections = result.document.get_annotations(AnnotationType.SECTION)
    print(f"Detected {len(sections)} clinical sections:")
    
    for section in sections:
        content = section.text.replace('\n', ' ').strip()[:100]
        print(f"\n{section.section_type}:")
        print(f"  {content}...")


def main():
    """Run all demos."""
    demo_default_pipeline()
    demo_fast_pipeline() 
    demo_custom_pipeline()
    demo_section_detection()
    
    print("\n=== PyTAKES Demo Complete ===")
    print("Try running with: python -m pytakes.cli annotate <text_file>")


if __name__ == "__main__":
    main()
