"""Base annotator class and interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..types import Annotation, Document


class Annotator(ABC):
    """Base class for all PyCTAKES annotators."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the annotator with optional configuration."""
        self.config = config or {}
        self.name = self.__class__.__name__
        self._is_initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the annotator (load models, resources, etc.)."""
        pass
    
    @abstractmethod
    def annotate(self, document: Document) -> List[Annotation]:
        """
        Annotate a document and return list of annotations.
        
        Args:
            document: The document to annotate
            
        Returns:
            List of annotations produced by this annotator
        """
        pass
    
    def preprocess(self, document: Document) -> Document:
        """
        Optional preprocessing step before annotation.
        
        Args:
            document: The document to preprocess
            
        Returns:
            The preprocessed document
        """
        return document
    
    def postprocess(self, document: Document, annotations: List[Annotation]) -> List[Annotation]:
        """
        Optional postprocessing step after annotation.
        
        Args:
            document: The original document
            annotations: The annotations produced by this annotator
            
        Returns:
            The postprocessed annotations
        """
        return annotations
    
    def process(self, document: Document) -> List[Annotation]:
        """
        Full processing pipeline: preprocess, annotate, postprocess.
        
        Args:
            document: The document to process
            
        Returns:
            List of annotations
        """
        if not self._is_initialized:
            self.initialize()
            self._is_initialized = True
        
        preprocessed_doc = self.preprocess(document)
        annotations = self.annotate(preprocessed_doc)
        return self.postprocess(document, annotations)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"
