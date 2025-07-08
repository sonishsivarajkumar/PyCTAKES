"""
PyCTAKES: Python-native clinical NLP framework.

A comprehensive clinical text processing pipeline that mirrors and extends
Apache cTAKES functionality with modern Python tooling.
"""

__version__ = "0.1.0"
__author__ = "Sonish Sivarajkumar"
__email__ = "sonish@example.com"
__license__ = "Apache-2.0"

from .pipeline import Pipeline
from .annotators.base import Annotator
from .types import Annotation, Document

# Convenience functions for creating common pipeline configurations
def create_default_pipeline(config=None):
    """Create a default clinical NLP pipeline."""
    return Pipeline.create_default_clinical_pipeline(config)

def create_fast_pipeline(config=None):
    """Create a fast pipeline optimized for speed."""
    return Pipeline.create_fast_pipeline(config)

def create_basic_pipeline(config=None):
    """Create a basic pipeline with minimal annotators."""
    return Pipeline.create_basic_pipeline(config)

__all__ = [
    "Pipeline",
    "Annotator", 
    "Annotation",
    "Document",
    "create_default_pipeline",
    "create_fast_pipeline", 
    "create_basic_pipeline"
]
