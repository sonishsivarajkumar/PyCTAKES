"""Test the base annotator class."""

import pytest
from pyctakes.annotators.base import Annotator
from pyctakes.types import Document, Annotation, Span, AnnotationType


class ConcreteAnnotator(Annotator):
    """Concrete implementation of Annotator for testing."""
    
    def initialize(self):
        """Initialize the annotator."""
        self.initialized = True
    
    def annotate(self, document: Document):
        """Create a simple annotation."""
        if len(document.text) > 0:
            span = Span(start=0, end=min(5, len(document.text)))
            annotation = Annotation(
                span=span,
                text=document.text[span.start:span.end],
                annotation_type=AnnotationType.TOKEN
            )
            return [annotation]
        return []


class TestAnnotator:
    """Test Annotator base class."""
    
    def test_annotator_creation(self):
        """Test creating an annotator."""
        annotator = ConcreteAnnotator()
        assert annotator.config == {}
        assert annotator.name == "ConcreteAnnotator"
        assert not annotator._is_initialized
    
    def test_annotator_with_config(self):
        """Test creating an annotator with configuration."""
        config = {"model_path": "/path/to/model", "threshold": 0.5}
        annotator = ConcreteAnnotator(config=config)
        
        assert annotator.config == config
        assert annotator.get_config("model_path") == "/path/to/model"
        assert annotator.get_config("threshold") == 0.5
        assert annotator.get_config("missing_key") is None
        assert annotator.get_config("missing_key", "default") == "default"
    
    def test_set_config(self):
        """Test setting configuration values."""
        annotator = ConcreteAnnotator()
        annotator.set_config("new_key", "new_value")
        
        assert annotator.get_config("new_key") == "new_value"
    
    def test_process_flow(self):
        """Test the complete process flow."""
        annotator = ConcreteAnnotator()
        document = Document(text="Hello world", doc_id="test")
        
        # Process should initialize, then annotate
        annotations = annotator.process(document)
        
        assert annotator._is_initialized
        assert hasattr(annotator, 'initialized')
        assert annotator.initialized
        assert len(annotations) == 1
        assert annotations[0].text == "Hello"
    
    def test_preprocess_postprocess(self):
        """Test preprocessing and postprocessing hooks."""
        
        class CustomAnnotator(ConcreteAnnotator):
            def preprocess(self, document):
                # Add metadata during preprocessing
                document.metadata["preprocessed"] = True
                return document
            
            def postprocess(self, document, annotations):
                # Modify annotations during postprocessing
                for ann in annotations:
                    ann.metadata["postprocessed"] = True
                return annotations
        
        annotator = CustomAnnotator()
        document = Document(text="Hello world", doc_id="test")
        
        annotations = annotator.process(document)
        
        assert document.metadata.get("preprocessed") is True
        assert len(annotations) == 1
        assert annotations[0].metadata.get("postprocessed") is True
    
    def test_repr(self):
        """Test string representation."""
        config = {"key": "value"}
        annotator = ConcreteAnnotator(config=config)
        
        repr_str = repr(annotator)
        assert "ConcreteAnnotator" in repr_str
        assert "config" in repr_str
