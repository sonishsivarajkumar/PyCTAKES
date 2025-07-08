"""Core PyCTAKES pipeline implementation."""

import time
from typing import Any, Dict, List, Optional, Union

from .annotators.base import Annotator
from .types import Document, ProcessingResult


class Pipeline:
    """
    Main PyCTAKES processing pipeline.
    
    The pipeline orchestrates multiple annotators to process clinical text
    from raw input through tokenization, NER, concept mapping, and relation extraction.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Pipeline configuration dictionary
        """
        self.config = config or {}
        self.annotators: List[Annotator] = []
        self._is_initialized = False

    @classmethod
    def create_default_clinical_pipeline(cls, config: Optional[Dict[str, Any]] = None) -> "Pipeline":
        """
        Create a default clinical NLP pipeline with standard annotators.
        
        Args:
            config: Optional configuration overrides
            
        Returns:
            Configured Pipeline instance
        """
        from .annotators.tokenization import ClinicalSentenceSegmenter, ClinicalTokenizer
        from .annotators.sections import ClinicalSectionAnnotator
        from .annotators.ner import ClinicalNERAnnotator
        from .annotators.assertion import NegationAssertionAnnotator
        from .annotators.umls import UMLSConceptMapper
        
        pipeline = cls(config)
        
        # Default configuration for each annotator
        default_config = config or {}
        
        # Add annotators in processing order
        pipeline.add_annotator(ClinicalSentenceSegmenter(
            default_config.get("sentence_segmenter", {})
        ))
        
        pipeline.add_annotator(ClinicalTokenizer(
            default_config.get("tokenizer", {})
        ))
        
        pipeline.add_annotator(ClinicalSectionAnnotator(
            default_config.get("section_detector", {})
        ))
        
        pipeline.add_annotator(ClinicalNERAnnotator(
            default_config.get("ner", {})
        ))
        
        pipeline.add_annotator(NegationAssertionAnnotator(
            default_config.get("assertion", {})
        ))
        
        pipeline.add_annotator(UMLSConceptMapper(
            default_config.get("concept_mapping", {})
        ))
        
        return pipeline

    @classmethod 
    def create_fast_pipeline(cls, config: Optional[Dict[str, Any]] = None) -> "Pipeline":
        """
        Create a fast pipeline optimized for speed over accuracy.
        
        Args:
            config: Optional configuration overrides
            
        Returns:
            Configured Pipeline instance for fast processing
        """
        from .annotators.tokenization import ClinicalSentenceSegmenter, ClinicalTokenizer
        from .annotators.ner import SimpleClinicalNER
        from .annotators.umls import SimpleDictionaryMapper
        
        pipeline = cls(config)
        
        # Fast tokenization without POS/lemma
        pipeline.add_annotator(ClinicalSentenceSegmenter({"backend": "rule"}))
        pipeline.add_annotator(ClinicalTokenizer({
            "backend": "rule", 
            "include_pos": False, 
            "include_lemma": False
        }))
        
        # Simple rule-based NER
        pipeline.add_annotator(SimpleClinicalNER())
        
        # Simple dictionary mapping
        pipeline.add_annotator(SimpleDictionaryMapper())
        
        return pipeline

    @classmethod
    def create_basic_pipeline(cls, config: Optional[Dict[str, Any]] = None) -> "Pipeline":
        """
        Create a basic pipeline with minimal annotators for simple use cases.
        
        Args:
            config: Optional configuration overrides
            
        Returns:
            Configured Pipeline instance with basic annotators
        """
        from .annotators.tokenization import ClinicalSentenceSegmenter, ClinicalTokenizer
        from .annotators.ner import ClinicalNERAnnotator
        
        pipeline = cls(config)
        
        # Use rule-based backend by default for reliability
        default_config = config or {}
        
        pipeline.add_annotator(ClinicalSentenceSegmenter(
            default_config.get("sentence_segmenter", {"backend": "rule"})
        ))
        pipeline.add_annotator(ClinicalTokenizer(
            default_config.get("tokenizer", {
                "backend": "rule", 
                "include_pos": False, 
                "include_lemma": False
            })
        ))
        pipeline.add_annotator(ClinicalNERAnnotator(
            default_config.get("ner", {"use_model": False, "use_rules": True})
        ))
        
        return pipeline
    
    def add_annotator(self, annotator: Annotator) -> "Pipeline":
        """
        Add an annotator to the pipeline.
        
        Args:
            annotator: The annotator to add
            
        Returns:
            Self for method chaining
        """
        self.annotators.append(annotator)
        return self
    
    def remove_annotator(self, annotator_name: str) -> "Pipeline":
        """
        Remove an annotator from the pipeline by name.
        
        Args:
            annotator_name: Name of the annotator to remove
            
        Returns:
            Self for method chaining
        """
        self.annotators = [
            ann for ann in self.annotators 
            if ann.name != annotator_name
        ]
        return self
    
    def initialize(self) -> None:
        """Initialize all annotators in the pipeline."""
        for annotator in self.annotators:
            if not annotator._is_initialized:
                annotator.initialize()
                annotator._is_initialized = True
        self._is_initialized = True
    
    def process_text(self, text: str, doc_id: Optional[str] = None) -> ProcessingResult:
        """
        Process raw text through the pipeline.
        
        Args:
            text: The clinical text to process
            doc_id: Optional document identifier
            
        Returns:
            ProcessingResult containing the annotated document and metadata
        """
        document = Document(text=text, doc_id=doc_id)
        return self.process_document(document)
    
    def process_document(self, document: Document) -> ProcessingResult:
        """
        Process a document through the pipeline.
        
        Args:
            document: The document to process
            
        Returns:
            ProcessingResult containing the annotated document and metadata
        """
        start_time = time.time()
        errors = []
        
        if not self._is_initialized:
            self.initialize()
        
        # Process through each annotator in sequence
        for annotator in self.annotators:
            try:
                annotations = annotator.process(document)
                document.annotations.extend(annotations)
            except Exception as e:
                error_msg = f"Error in {annotator.name}: {str(e)}"
                errors.append(error_msg)
                if self.config.get("fail_on_error", False):
                    raise RuntimeError(error_msg) from e
        
        processing_time = time.time() - start_time
        
        return ProcessingResult(
            document=document,
            processing_time=processing_time,
            pipeline_config=self.config,
            errors=errors
        )
    
    def batch_process(self, texts: List[str]) -> List[ProcessingResult]:
        """
        Process multiple texts in batch.
        
        Args:
            texts: List of text strings to process
            
        Returns:
            List of ProcessingResult objects
        """
        results = []
        for i, text in enumerate(texts):
            doc_id = f"doc_{i}"
            result = self.process_text(text, doc_id=doc_id)
            results.append(result)
        return results
    
    def __call__(self, text: str) -> Document:
        """
        Convenience method for processing text.
        
        Args:
            text: The text to process
            
        Returns:
            The annotated document
        """
        result = self.process_text(text)
        return result.document
    
    def get_annotator(self, name: str) -> Optional[Annotator]:
        """
        Get an annotator by name.
        
        Args:
            name: Name of the annotator
            
        Returns:
            The annotator if found, None otherwise
        """
        for annotator in self.annotators:
            if annotator.name == name:
                return annotator
        return None
    
    def list_annotators(self) -> List[str]:
        """
        Get list of annotator names in the pipeline.
        
        Returns:
            List of annotator names
        """
        return [annotator.name for annotator in self.annotators]
    
    def __repr__(self) -> str:
        annotator_names = ", ".join(self.list_annotators())
        return f"Pipeline(annotators=[{annotator_names}])"
