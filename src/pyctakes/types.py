"""Core data types for PyCTAKES."""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class AnnotationType(Enum):
    """Types of annotations supported by PyCTAKES."""
    TOKEN = "token"
    SENTENCE = "sentence"
    SECTION = "section"
    NAMED_ENTITY = "named_entity"
    CONCEPT = "concept"
    ASSERTION = "assertion"
    RELATION = "relation"
    TEMPORAL = "temporal"


class EntityType(Enum):
    """Clinical entity types."""
    DISORDER = "disorder"
    MEDICATION = "medication"
    PROCEDURE = "procedure"
    ANATOMY = "anatomy"
    SIGN_SYMPTOM = "sign_symptom"
    LAB_VALUE = "lab_value"
    PERSON = "person"
    ORGANIZATION = "organization"


class AssertionType(Enum):
    """Assertion types for clinical concepts."""
    PRESENT = "present"
    ABSENT = "absent"
    POSSIBLE = "possible"
    CONDITIONAL = "conditional"
    HYPOTHETICAL = "hypothetical"
    FAMILY_HISTORY = "family_history"
    HISTORICAL = "historical"


@dataclass
class Span:
    """Text span with start and end positions."""
    start: int
    end: int
    
    def __len__(self) -> int:
        return self.end - self.start
    
    def overlaps(self, other: "Span") -> bool:
        """Check if this span overlaps with another."""
        return self.start < other.end and self.end > other.start


@dataclass
class Annotation:
    """Base annotation class for all PyCTAKES annotations."""
    span: Span
    text: str
    annotation_type: AnnotationType
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def start(self) -> int:
        return self.span.start
    
    @property
    def end(self) -> int:
        return self.span.end


@dataclass
class TokenAnnotation(Annotation):
    """Token-level annotation."""
    pos_tag: Optional[str] = None
    lemma: Optional[str] = None
    is_stop: bool = False
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.TOKEN:
            self.annotation_type = AnnotationType.TOKEN


@dataclass
class SentenceAnnotation(Annotation):
    """Sentence-level annotation."""
    tokens: List[TokenAnnotation] = field(default_factory=list)
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.SENTENCE:
            self.annotation_type = AnnotationType.SENTENCE


@dataclass
class SectionAnnotation(Annotation):
    """Clinical section annotation (e.g., History, ROS, Medications)."""
    section_type: str = ""
    section_id: Optional[str] = None
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.SECTION:
            self.annotation_type = AnnotationType.SECTION


@dataclass
class NamedEntityAnnotation(Annotation):
    """Named entity annotation."""
    entity_type: EntityType = EntityType.DISORDER
    entity_subtype: Optional[str] = None
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.NAMED_ENTITY:
            self.annotation_type = AnnotationType.NAMED_ENTITY


@dataclass
class ConceptAnnotation(Annotation):
    """UMLS concept annotation."""
    concept_code: str = ""
    concept_name: str = ""
    semantic_type: str = ""
    vocabulary: str = "UMLS"
    assertion: AssertionType = AssertionType.PRESENT
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.CONCEPT:
            self.annotation_type = AnnotationType.CONCEPT


@dataclass
class RelationAnnotation(Annotation):
    """Relation between two annotations."""
    relation_type: str = ""
    arg1: Optional[Annotation] = None
    arg2: Optional[Annotation] = None
    direction: str = "bidirectional"  # "forward", "backward", "bidirectional"
    
    def __post_init__(self):
        if self.annotation_type != AnnotationType.RELATION:
            self.annotation_type = AnnotationType.RELATION


@dataclass
class Document:
    """Clinical document with text and annotations."""
    text: str
    doc_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    annotations: List[Annotation] = field(default_factory=list)
    
    def add_annotation(self, annotation: Annotation) -> None:
        """Add an annotation to the document."""
        self.annotations.append(annotation)
    
    def get_annotations(self, annotation_type: AnnotationType) -> List[Annotation]:
        """Get all annotations of a specific type."""
        return [ann for ann in self.annotations if ann.annotation_type == annotation_type]
    
    def get_annotations_in_span(self, span: Span) -> List[Annotation]:
        """Get all annotations that overlap with the given span."""
        return [ann for ann in self.annotations if ann.span.overlaps(span)]
    
    def get_text_span(self, span: Span) -> str:
        """Extract text for a given span."""
        return self.text[span.start:span.end]


@dataclass
class ProcessingResult:
    """Result of processing a document through the pipeline."""
    document: Document
    processing_time: float
    pipeline_config: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
