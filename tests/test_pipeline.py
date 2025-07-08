"""Test the pipeline functionality."""

import pytest
from pyctakes.pipeline import Pipeline
from pyctakes.annotators.base import Annotator
from pyctakes.types import Document, Annotation, Span, AnnotationType


class MockAnnotator(Annotator):
    """Mock annotator for testing."""
    
    def initialize(self):
        """Initialize the mock annotator."""
        pass
    
    def annotate(self, document: Document):
        """Create a mock annotation."""
        span = Span(start=0, end=7)
        annotation = Annotation(
            span=span,
            text="Patient",
            annotation_type=AnnotationType.TOKEN,
            confidence=1.0
        )
        return [annotation]


class TestPipeline:
    """Test Pipeline class."""
    
    def test_pipeline_creation(self):
        """Test creating a pipeline."""
        pipeline = Pipeline()
        assert len(pipeline.annotators) == 0
        assert not pipeline._is_initialized
    
    def test_add_annotator(self):
        """Test adding annotators to pipeline."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        
        pipeline.add_annotator(annotator)
        assert len(pipeline.annotators) == 1
        assert pipeline.annotators[0] == annotator
    
    def test_remove_annotator(self):
        """Test removing annotators from pipeline."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        
        pipeline.add_annotator(annotator)
        pipeline.remove_annotator("MockAnnotator")
        assert len(pipeline.annotators) == 0
    
    def test_process_text(self):
        """Test processing text through pipeline."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        pipeline.add_annotator(annotator)
        
        text = "Patient has diabetes."
        result = pipeline.process_text(text, doc_id="test_001")
        
        assert result.document.text == text
        assert result.document.doc_id == "test_001"
        assert len(result.document.annotations) == 1
        assert result.document.annotations[0].text == "Patient"
        assert result.processing_time > 0
    
    def test_process_document(self):
        """Test processing a document through pipeline."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        pipeline.add_annotator(annotator)
        
        document = Document(text="Patient has diabetes.", doc_id="test_001")
        result = pipeline.process_document(document)
        
        assert result.document == document
        assert len(result.document.annotations) == 1
        assert result.processing_time > 0
    
    def test_batch_process(self):
        """Test batch processing multiple texts."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        pipeline.add_annotator(annotator)
        
        texts = ["Patient has diabetes.", "Patient has hypertension."]
        results = pipeline.batch_process(texts)
        
        assert len(results) == 2
        for i, result in enumerate(results):
            assert result.document.text == texts[i]
            assert result.document.doc_id == f"doc_{i}"
            assert len(result.document.annotations) == 1
    
    def test_callable_interface(self):
        """Test using pipeline as a callable."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        pipeline.add_annotator(annotator)
        
        text = "Patient has diabetes."
        document = pipeline(text)
        
        assert isinstance(document, Document)
        assert document.text == text
        assert len(document.annotations) == 1
    
    def test_list_annotators(self):
        """Test listing annotators in pipeline."""
        pipeline = Pipeline()
        annotator1 = MockAnnotator()
        
        # Create a second mock annotator with a different name
        class AnotherMockAnnotator(Annotator):
            def initialize(self): pass
            def annotate(self, document): return []
        
        annotator2 = AnotherMockAnnotator()
        
        pipeline.add_annotator(annotator1)
        pipeline.add_annotator(annotator2)
        
        names = pipeline.list_annotators()
        assert "MockAnnotator" in names
        assert "AnotherMockAnnotator" in names
        assert len(names) == 2
    
    def test_get_annotator(self):
        """Test getting annotator by name."""
        pipeline = Pipeline()
        annotator = MockAnnotator()
        pipeline.add_annotator(annotator)
        
        retrieved = pipeline.get_annotator("MockAnnotator")
        assert retrieved == annotator
        
        not_found = pipeline.get_annotator("NonExistentAnnotator")
        assert not_found is None
