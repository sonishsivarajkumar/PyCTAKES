"""Example usage of PyTAKES framework."""

from pytakes import Pipeline
from pytakes.annotators.base import Annotator
from pytakes.types import (
    Document, Annotation, Span, AnnotationType, 
    EntityType, NamedEntityAnnotation
)
import re


class SimpleTokenAnnotator(Annotator):
    """Simple tokenizer that splits on whitespace."""
    
    def initialize(self):
        """Initialize the tokenizer."""
        self.pattern = re.compile(r'\S+')
    
    def annotate(self, document: Document):
        """Tokenize the document."""
        annotations = []
        for match in self.pattern.finditer(document.text):
            span = Span(start=match.start(), end=match.end())
            annotation = Annotation(
                span=span,
                text=match.group(),
                annotation_type=AnnotationType.TOKEN,
                confidence=1.0
            )
            annotations.append(annotation)
        return annotations


class SimpleMedicalNERAnnotator(Annotator):
    """Simple medical NER using keyword matching."""
    
    def initialize(self):
        """Initialize the NER annotator."""
        self.medical_terms = {
            'diabetes': EntityType.DISORDER,
            'hypertension': EntityType.DISORDER,
            'metformin': EntityType.MEDICATION,
            'lisinopril': EntityType.MEDICATION,
            'chest pain': EntityType.SIGN_SYMPTOM,
            'shortness of breath': EntityType.SIGN_SYMPTOM,
        }
    
    def annotate(self, document: Document):
        """Find medical entities in the document."""
        annotations = []
        text_lower = document.text.lower()
        
        for term, entity_type in self.medical_terms.items():
            start = 0
            while True:
                pos = text_lower.find(term, start)
                if pos == -1:
                    break
                
                span = Span(start=pos, end=pos + len(term))
                annotation = NamedEntityAnnotation(
                    span=span,
                    text=document.text[pos:pos + len(term)],
                    annotation_type=AnnotationType.NAMED_ENTITY,
                    entity_type=entity_type,
                    confidence=0.9
                )
                annotations.append(annotation)
                start = pos + 1
        
        return annotations


def main():
    """Demonstrate PyTAKES usage."""
    
    # Sample clinical text
    clinical_text = """
    Patient is a 45-year-old male with diabetes mellitus and hypertension.
    He denies chest pain or shortness of breath.
    Current medications include metformin and lisinopril.
    """
    
    print("=== PyTAKES Demo ===")
    print(f"Input Text: {clinical_text.strip()}")
    print()
    
    # Create and configure pipeline
    pipeline = Pipeline()
    pipeline.add_annotator(SimpleTokenAnnotator())
    pipeline.add_annotator(SimpleMedicalNERAnnotator())
    
    # Process the text
    result = pipeline.process_text(clinical_text, doc_id="demo_001")
    
    print(f"Processing Time: {result.processing_time:.3f} seconds")
    print(f"Total Annotations: {len(result.document.annotations)}")
    print()
    
    # Display tokens
    tokens = result.document.get_annotations(AnnotationType.TOKEN)
    print(f"Tokens ({len(tokens)}):")
    for token in tokens[:10]:  # Show first 10 tokens
        print(f"  {token.start:3d}-{token.end:3d}: '{token.text}'")
    if len(tokens) > 10:
        print(f"  ... and {len(tokens) - 10} more")
    print()
    
    # Display medical entities
    entities = result.document.get_annotations(AnnotationType.NAMED_ENTITY)
    print(f"Medical Entities ({len(entities)}):")
    for entity in entities:
        if hasattr(entity, 'entity_type'):
            print(f"  {entity.start:3d}-{entity.end:3d}: '{entity.text}' -> {entity.entity_type.value}")
        else:
            print(f"  {entity.start:3d}-{entity.end:3d}: '{entity.text}'")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
