#!/usr/bin/env python3
"""
PyTAKES Quick Start Example

This example demonstrates the basic usage of PyTAKES for clinical text processing.
"""

from pytakes import Pipeline
from pytakes.types import Document

def main():
    print("🏥 PyTAKES Quick Start Example")
    print("=" * 50)
    
    # Initialize the pipeline
    print("\n1. Initializing PyTAKES pipeline...")
    pipeline = Pipeline()
    
    # Sample clinical text
    clinical_text = """
    CHIEF COMPLAINT: Chest pain and shortness of breath.
    
    HISTORY OF PRESENT ILLNESS:
    Patient is a 65-year-old male with a history of diabetes mellitus type 2 
    and hypertension who presents with acute onset chest pain. He denies any 
    previous myocardial infarction. Current medications include metformin 500mg 
    twice daily and lisinopril 10mg daily.
    
    PHYSICAL EXAMINATION:
    Blood pressure: 150/90 mmHg
    Heart rate: 88 bpm
    No acute distress noted.
    
    ASSESSMENT AND PLAN:
    1. Rule out acute coronary syndrome - will obtain EKG and cardiac enzymes
    2. Continue current diabetes management
    3. Consider adjustment of antihypertensive medication
    """
    
    print(f"\n2. Processing clinical text ({len(clinical_text)} characters)...")
    
    # Process the text
    result = pipeline.process_text(clinical_text, doc_id="example_001")
    
    print(f"\n3. Processing completed in {result.processing_time:.3f} seconds")
    print(f"   Found {len(result.document.annotations)} annotations")
    
    # Display results (currently empty since we haven't added annotators yet)
    if result.document.annotations:
        print("\n4. Annotations found:")
        for i, annotation in enumerate(result.document.annotations, 1):
            print(f"   {i}. [{annotation.start}-{annotation.end}] "
                  f"'{annotation.text}' -> {annotation.annotation_type.value}")
    else:
        print("\n4. No annotations found (no annotators configured)")
        print("   💡 To see annotations, you'll need to add annotators to the pipeline")
    
    # Show document metadata
    print(f"\n5. Document metadata:")
    print(f"   - Document ID: {result.document.doc_id}")
    print(f"   - Text length: {len(result.document.text)} characters")
    print(f"   - Pipeline config: {result.pipeline_config}")
    
    if result.errors:
        print(f"\n⚠️  Errors encountered: {result.errors}")
    else:
        print("\n✅ Processing completed successfully!")
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("- Add annotators to the pipeline for NER, concept mapping, etc.")
    print("- Explore the CLI: `pytakes --help`")
    print("- Check out the documentation for advanced features")


if __name__ == "__main__":
    main()
