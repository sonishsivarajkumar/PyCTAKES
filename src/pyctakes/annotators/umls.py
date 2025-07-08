"""UMLS concept mapping annotator."""

import re
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass

from ..types import (
    Document, Annotation, Span, AnnotationType, 
    ConceptAnnotation, NamedEntityAnnotation, EntityType
)
from .base import Annotator


@dataclass
class UMLSConcept:
    """UMLS concept information."""
    cui: str
    preferred_name: str
    semantic_types: List[str]
    vocabulary: str = "UMLS"
    synonyms: List[str] = None
    
    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []


class UMLSConceptMapper(Annotator):
    """Map clinical entities to UMLS concepts using dictionary lookup."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.concept_dictionary = {}
        self.use_approximate_matching = self.get_config("use_approximate_matching", True)
        self.min_similarity = self.get_config("min_similarity", 0.8)
        self.case_sensitive = self.get_config("case_sensitive", False)
        
        # Load concept mappings
        self._load_concept_mappings()
    
    def _load_concept_mappings(self):
        """Load UMLS concept mappings (simplified version)."""
        # In a real implementation, this would load from UMLS files
        # Here we provide a basic set of common clinical concepts
        
        concepts = [
            # Disorders
            UMLSConcept(
                cui="C0011847",
                preferred_name="Diabetes Mellitus",
                semantic_types=["T047"],  # Disease or Syndrome
                synonyms=["diabetes", "diabetes mellitus", "dm"]
            ),
            UMLSConcept(
                cui="C0020538",
                preferred_name="Hypertensive disease",
                semantic_types=["T047"],
                synonyms=["hypertension", "high blood pressure", "htn"]
            ),
            UMLSConcept(
                cui="C0003873",
                preferred_name="Rheumatoid Arthritis",
                semantic_types=["T047"],
                synonyms=["rheumatoid arthritis", "ra"]
            ),
            UMLSConcept(
                cui="C0004096",
                preferred_name="Asthma",
                semantic_types=["T047"],
                synonyms=["asthma", "bronchial asthma"]
            ),
            UMLSConcept(
                cui="C0011570",
                preferred_name="Mental Depression",
                semantic_types=["T048"],  # Mental or Behavioral Dysfunction
                synonyms=["depression", "major depression", "clinical depression"]
            ),
            UMLSConcept(
                cui="C0028754",
                preferred_name="Obesity",
                semantic_types=["T047"],
                synonyms=["obesity", "obese"]
            ),
            UMLSConcept(
                cui="C0002895",
                preferred_name="Anemia",
                semantic_types=["T047"],
                synonyms=["anemia", "anaemia"]
            ),
            
            # Medications
            UMLSConcept(
                cui="C0025598",
                preferred_name="Metformin",
                semantic_types=["T109", "T121"],  # Organic Chemical, Pharmacologic Substance
                vocabulary="RxNorm",
                synonyms=["metformin", "glucophage"]
            ),
            UMLSConcept(
                cui="C0021641",
                preferred_name="Insulin",
                semantic_types=["T116", "T121", "T125"],  # Amino Acid, Peptide, or Protein; Pharmacologic Substance; Hormone
                vocabulary="RxNorm",
                synonyms=["insulin"]
            ),
            UMLSConcept(
                cui="C0065374",
                preferred_name="Lisinopril",
                semantic_types=["T109", "T121"],
                vocabulary="RxNorm",
                synonyms=["lisinopril", "prinivil", "zestril"]
            ),
            UMLSConcept(
                cui="C0004057",
                preferred_name="Aspirin",
                semantic_types=["T109", "T121"],
                vocabulary="RxNorm",
                synonyms=["aspirin", "acetylsalicylic acid", "asa"]
            ),
            UMLSConcept(
                cui="C0004454",
                preferred_name="Atorvastatin",
                semantic_types=["T109", "T121"],
                vocabulary="RxNorm",
                synonyms=["atorvastatin", "lipitor"]
            ),
            
            # Procedures
            UMLSConcept(
                cui="C0009378",
                preferred_name="Colonoscopy",
                semantic_types=["T060"],  # Diagnostic Procedure
                synonyms=["colonoscopy", "colonic endoscopy"]
            ),
            UMLSConcept(
                cui="C0003968",
                preferred_name="Appendectomy",
                semantic_types=["T061"],  # Therapeutic or Preventive Procedure
                synonyms=["appendectomy", "appendicectomy"]
            ),
            UMLSConcept(
                cui="C0007430",
                preferred_name="Cardiac Catheterization",
                semantic_types=["T060"],
                synonyms=["cardiac catheterization", "heart catheterization"]
            ),
            
            # Anatomy
            UMLSConcept(
                cui="C0018787",
                preferred_name="Heart",
                semantic_types=["T023"],  # Body Part, Organ, or Organ Component
                synonyms=["heart", "cardiac"]
            ),
            UMLSConcept(
                cui="C0024109",
                preferred_name="Lung",
                semantic_types=["T023"],
                synonyms=["lung", "lungs", "pulmonary"]
            ),
            UMLSConcept(
                cui="C0023884",
                preferred_name="Liver",
                semantic_types=["T023"],
                synonyms=["liver", "hepatic"]
            ),
            UMLSConcept(
                cui="C0022646",
                preferred_name="Kidney",
                semantic_types=["T023"],
                synonyms=["kidney", "kidneys", "renal"]
            ),
            
            # Signs and Symptoms
            UMLSConcept(
                cui="C0013404",
                preferred_name="Dyspnea",
                semantic_types=["T184"],  # Sign or Symptom
                synonyms=["dyspnea", "shortness of breath", "sob", "difficulty breathing"]
            ),
            UMLSConcept(
                cui="C0008031",
                preferred_name="Chest Pain",
                semantic_types=["T184"],
                synonyms=["chest pain", "chest discomfort"]
            ),
            UMLSConcept(
                cui="C0015967",
                preferred_name="Fever",
                semantic_types=["T184"],
                synonyms=["fever", "pyrexia", "febrile"]
            ),
            UMLSConcept(
                cui="C0027497",
                preferred_name="Nausea",
                semantic_types=["T184"],
                synonyms=["nausea", "nauseated", "sick to stomach"]
            ),
        ]
        
        # Build lookup dictionary
        for concept in concepts:
            # Index by preferred name and synonyms
            terms_to_index = [concept.preferred_name] + concept.synonyms
            
            for term in terms_to_index:
                term_key = term.lower() if not self.case_sensitive else term
                if term_key not in self.concept_dictionary:
                    self.concept_dictionary[term_key] = []
                self.concept_dictionary[term_key].append(concept)
    
    def initialize(self):
        """Initialize the concept mapper."""
        pass
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Map entities to UMLS concepts."""
        # Get existing named entities
        entities = document.get_annotations(AnnotationType.NAMED_ENTITY)
        
        concept_annotations = []
        
        for entity in entities:
            if isinstance(entity, NamedEntityAnnotation):
                concepts = self._find_concepts(entity.text, entity.entity_type)
                
                for concept, confidence in concepts:
                    concept_annotation = ConceptAnnotation(
                        span=entity.span,
                        text=entity.text,
                        annotation_type=AnnotationType.CONCEPT,
                        concept_code=concept.cui,
                        concept_name=concept.preferred_name,
                        semantic_type=", ".join(concept.semantic_types),
                        vocabulary=concept.vocabulary,
                        confidence=confidence,
                        metadata={
                            "original_entity_type": entity.entity_type.value,
                            "matching_term": self._find_matching_term(entity.text, concept),
                            "source_entity": entity
                        }
                    )
                    concept_annotations.append(concept_annotation)
        
        return concept_annotations
    
    def _find_concepts(self, text: str, entity_type: EntityType) -> List[Tuple[UMLSConcept, float]]:
        """Find UMLS concepts for given text."""
        text_key = text.lower() if not self.case_sensitive else text
        matches = []
        
        # Exact match
        if text_key in self.concept_dictionary:
            for concept in self.concept_dictionary[text_key]:
                if self._is_compatible_type(entity_type, concept):
                    matches.append((concept, 0.95))
        
        # Approximate matching
        if self.use_approximate_matching and not matches:
            for term, concepts in self.concept_dictionary.items():
                similarity = self._calculate_similarity(text_key, term)
                if similarity >= self.min_similarity:
                    for concept in concepts:
                        if self._is_compatible_type(entity_type, concept):
                            matches.append((concept, similarity * 0.9))
        
        # Sort by confidence
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Return top matches
        return matches[:3]  # Limit to top 3 matches
    
    def _is_compatible_type(self, entity_type: EntityType, concept: UMLSConcept) -> bool:
        """Check if entity type is compatible with concept semantic types."""
        # Map entity types to semantic type patterns
        type_mappings = {
            EntityType.DISORDER: ["T047", "T048", "T049", "T050", "T184"],  # Disease, Mental Dysfunction, Sign/Symptom
            EntityType.MEDICATION: ["T109", "T121", "T125", "T116"],  # Chemical, Pharmacologic, Hormone, Protein
            EntityType.PROCEDURE: ["T060", "T061"],  # Diagnostic/Therapeutic Procedure
            EntityType.ANATOMY: ["T023", "T024", "T025", "T026", "T029", "T030"],  # Body parts
            EntityType.SIGN_SYMPTOM: ["T184", "T033"],  # Sign/Symptom, Finding
            EntityType.LAB_VALUE: ["T033", "T034", "T059"],  # Finding, Laboratory/Test Result
        }
        
        compatible_types = type_mappings.get(entity_type, [])
        
        # Check if any semantic type matches
        for sem_type in concept.semantic_types:
            if sem_type in compatible_types:
                return True
        
        return True  # Default to compatible if no specific mapping
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simple implementation)."""
        # Simple Jaccard similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _find_matching_term(self, text: str, concept: UMLSConcept) -> str:
        """Find which term in the concept matched the input text."""
        text_key = text.lower() if not self.case_sensitive else text
        
        # Check preferred name
        if concept.preferred_name.lower() == text_key:
            return concept.preferred_name
        
        # Check synonyms
        for synonym in concept.synonyms:
            if synonym.lower() == text_key:
                return synonym
        
        # Return preferred name as fallback
        return concept.preferred_name
    
    def get_concept_info(self, cui: str) -> Optional[UMLSConcept]:
        """Get concept information by CUI."""
        for concepts in self.concept_dictionary.values():
            for concept in concepts:
                if concept.cui == cui:
                    return concept
        return None
    
    def search_concepts(self, query: str, max_results: int = 10) -> List[Tuple[UMLSConcept, float]]:
        """Search for concepts by query string."""
        query_key = query.lower() if not self.case_sensitive else query
        matches = []
        
        for term, concepts in self.concept_dictionary.items():
            if query_key in term or term in query_key:
                similarity = self._calculate_similarity(query_key, term)
                for concept in concepts:
                    matches.append((concept, similarity))
        
        # Sort by confidence and remove duplicates
        seen_cuis = set()
        unique_matches = []
        for concept, score in sorted(matches, key=lambda x: x[1], reverse=True):
            if concept.cui not in seen_cuis:
                unique_matches.append((concept, score))
                seen_cuis.add(concept.cui)
        
        return unique_matches[:max_results]


class SimpleDictionaryMapper(Annotator):
    """Simple dictionary-based concept mapper for basic use cases."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.mappings = {
            "diabetes": ("C0011847", "Diabetes Mellitus"),
            "hypertension": ("C0020538", "Hypertensive disease"),
            "high blood pressure": ("C0020538", "Hypertensive disease"),
            "asthma": ("C0004096", "Asthma"),
            "depression": ("C0011570", "Mental Depression"),
            "metformin": ("C0025598", "Metformin"),
            "insulin": ("C0021641", "Insulin"),
            "aspirin": ("C0004057", "Aspirin"),
        }
    
    def initialize(self):
        """Initialize simple mapper."""
        pass
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Simple concept mapping."""
        entities = document.get_annotations(AnnotationType.NAMED_ENTITY)
        concepts = []
        
        for entity in entities:
            if isinstance(entity, NamedEntityAnnotation):
                text_lower = entity.text.lower()
                if text_lower in self.mappings:
                    cui, name = self.mappings[text_lower]
                    concept = ConceptAnnotation(
                        span=entity.span,
                        text=entity.text,
                        annotation_type=AnnotationType.CONCEPT,
                        concept_code=cui,
                        concept_name=name,
                        semantic_type="T047",  # Generic
                        vocabulary="UMLS",
                        confidence=0.9
                    )
                    concepts.append(concept)
        
        return concepts
