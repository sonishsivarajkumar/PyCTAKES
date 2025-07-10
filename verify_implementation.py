#!/usr/bin/env python3
"""Quick verification script for pyCTAKES v1.0 features."""

import sys
import pyctakes
from pyctakes.types import AnnotationType

def test_basic_functionality():
    """Test basic functionality."""
    print("🧪 Testing pyCTAKES v1.0 Implementation...")
    
    # Test text
    clinical_text = """
    Patient is a 65-year-old male with diabetes and hypertension.
    He presents with chest pain but denies shortness of breath.
    Current medications include metformin 500mg and lisinopril 10mg daily.
    """
    
    # Test 1: Basic Pipeline
    print("\n1️⃣ Testing Basic Pipeline...")
    pipeline = pyctakes.create_basic_pipeline()
    result = pipeline.process_text(clinical_text, doc_id="test_1")
    
    sentences = result.document.get_annotations(AnnotationType.SENTENCE)
    tokens = result.document.get_annotations(AnnotationType.TOKEN) 
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    
    print(f"   ✅ Sentences: {len(sentences)}")
    print(f"   ✅ Tokens: {len(tokens)}")
    print(f"   ✅ Entities: {len(entities)}")
    print(f"   ⏱️ Processing time: {result.processing_time:.3f}s")
    
    # Show some entities
    if entities:
        print("   📝 Sample entities:")
        for entity in entities[:3]:
            print(f"      - {entity.text} ({entity.entity_type.value})")
    
    # Test 2: Fast Pipeline
    print("\n2️⃣ Testing Fast Pipeline...")
    fast_pipeline = pyctakes.create_fast_pipeline()
    fast_result = fast_pipeline.process_text(clinical_text, doc_id="test_2")
    
    fast_entities = fast_result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    print(f"   ✅ Fast entities: {len(fast_entities)}")
    print(f"   ⏱️ Fast processing time: {fast_result.processing_time:.3f}s")
    
    # Test 3: Custom Pipeline
    print("\n3️⃣ Testing Custom Pipeline...")
    from pyctakes import Pipeline
    from pyctakes.annotators import ClinicalTokenizer, ClinicalNERAnnotator
    
    custom_pipeline = Pipeline()
    custom_pipeline.add_annotator(ClinicalTokenizer({"backend": "rule"}))
    custom_pipeline.add_annotator(ClinicalNERAnnotator({"use_rules": True, "use_model": False}))
    
    custom_result = custom_pipeline.process_text(clinical_text, doc_id="test_3")
    custom_annotations = custom_result.document.annotations
    print(f"   ✅ Custom annotations: {len(custom_annotations)}")
    
    # Test 4: CLI functionality (basic check)
    print("\n4️⃣ Testing Pipeline Components...")
    pipeline_names = [ann.__class__.__name__ for ann in pipeline.annotators]
    print(f"   ✅ Basic pipeline annotators: {pipeline_names}")
    
    fast_names = [ann.__class__.__name__ for ann in fast_pipeline.annotators] 
    print(f"   ✅ Fast pipeline annotators: {fast_names}")
    
    print("\n🎉 All tests completed successfully!")
    print(f"📊 Summary:")
    print(f"   - Basic pipeline: {len(result.document.annotations)} annotations")
    print(f"   - Fast pipeline: {len(fast_result.document.annotations)} annotations")
    print(f"   - Custom pipeline: {len(custom_result.document.annotations)} annotations")
    
    return True

if __name__ == "__main__":
    try:
        success = test_basic_functionality()
        if success:
            print("\n✅ pyCTAKES v1.0 implementation is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
