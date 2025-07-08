"""Test configuration for PyTAKES."""

import pytest
from pytakes.types import Document, Span, Annotation, AnnotationType


@pytest.fixture
def sample_text():
    """Sample clinical text for testing."""
    return """
    Patient is a 45-year-old male with diabetes mellitus and hypertension.
    He denies chest pain or shortness of breath.
    Current medications include metformin and lisinopril.
    """


@pytest.fixture
def sample_document(sample_text):
    """Sample document for testing."""
    return Document(text=sample_text, doc_id="test_doc_001")


@pytest.fixture
def sample_annotation():
    """Sample annotation for testing."""
    span = Span(start=20, end=35)
    return Annotation(
        span=span,
        text="45-year-old male",
        annotation_type=AnnotationType.NAMED_ENTITY,
        confidence=0.95
    )
