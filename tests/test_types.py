"""Test core types."""

import pytest
from pyctakes.types import (
    Span, Annotation, Document, AnnotationType, 
    EntityType, AssertionType, TokenAnnotation
)


class TestSpan:
    """Test Span class."""
    
    def test_span_creation(self):
        """Test creating a span."""
        span = Span(start=10, end=20)
        assert span.start == 10
        assert span.end == 20
        assert len(span) == 10
    
    def test_span_overlap(self):
        """Test span overlap detection."""
        span1 = Span(start=10, end=20)
        span2 = Span(start=15, end=25)
        span3 = Span(start=25, end=30)
        
        assert span1.overlaps(span2)
        assert span2.overlaps(span1)
        assert not span1.overlaps(span3)
        assert not span3.overlaps(span1)


class TestAnnotation:
    """Test Annotation class."""
    
    def test_annotation_creation(self):
        """Test creating an annotation."""
        span = Span(start=10, end=20)
        annotation = Annotation(
            span=span,
            text="test text",
            annotation_type=AnnotationType.TOKEN,
            confidence=0.95
        )
        
        assert annotation.span == span
        assert annotation.text == "test text"
        assert annotation.annotation_type == AnnotationType.TOKEN
        assert annotation.confidence == 0.95
        assert annotation.start == 10
        assert annotation.end == 20
    
    def test_token_annotation(self):
        """Test TokenAnnotation."""
        span = Span(start=0, end=5)
        token = TokenAnnotation(
            span=span,
            text="hello",
            annotation_type=AnnotationType.TOKEN,
            pos_tag="NN",
            lemma="hello",
            is_stop=False
        )
        
        assert token.pos_tag == "NN"
        assert token.lemma == "hello"
        assert not token.is_stop
        assert token.annotation_type == AnnotationType.TOKEN


class TestDocument:
    """Test Document class."""
    
    def test_document_creation(self):
        """Test creating a document."""
        text = "Patient has diabetes."
        doc = Document(text=text, doc_id="test_001")
        
        assert doc.text == text
        assert doc.doc_id == "test_001"
        assert len(doc.annotations) == 0
    
    def test_add_annotation(self):
        """Test adding annotations to a document."""
        doc = Document(text="Patient has diabetes.", doc_id="test_001")
        
        span = Span(start=12, end=20)
        annotation = Annotation(
            span=span,
            text="diabetes",
            annotation_type=AnnotationType.NAMED_ENTITY
        )
        
        doc.add_annotation(annotation)
        assert len(doc.annotations) == 1
        assert doc.annotations[0] == annotation
    
    def test_get_annotations_by_type(self):
        """Test getting annotations by type."""
        doc = Document(text="Patient has diabetes.", doc_id="test_001")
        
        # Add different types of annotations
        span1 = Span(start=0, end=7)
        ann1 = Annotation(span=span1, text="Patient", annotation_type=AnnotationType.TOKEN)
        
        span2 = Span(start=12, end=20)
        ann2 = Annotation(span=span2, text="diabetes", annotation_type=AnnotationType.NAMED_ENTITY)
        
        doc.add_annotation(ann1)
        doc.add_annotation(ann2)
        
        tokens = doc.get_annotations(AnnotationType.TOKEN)
        entities = doc.get_annotations(AnnotationType.NAMED_ENTITY)
        
        assert len(tokens) == 1
        assert len(entities) == 1
        assert tokens[0] == ann1
        assert entities[0] == ann2
    
    def test_get_text_span(self):
        """Test extracting text for a span."""
        text = "Patient has diabetes."
        doc = Document(text=text, doc_id="test_001")
        
        span = Span(start=12, end=20)
        extracted = doc.get_text_span(span)
        
        assert extracted == "diabetes"
