"""Negation and assertion detection annotator (pyConText-style)."""

import re
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

from ..types import (
    Document, Annotation, Span, AnnotationType, 
    AssertionType, NamedEntityAnnotation
)
from .base import Annotator


class ContextDirection(Enum):
    """Direction of context cues."""
    FORWARD = "forward"
    BACKWARD = "backward"
    BIDIRECTIONAL = "bidirectional"


class ContextCue:
    """A context cue with its properties."""
    
    def __init__(self, 
                 literal: str, 
                 category: str, 
                 direction: ContextDirection = ContextDirection.BIDIRECTIONAL,
                 max_distance: int = 10):
        self.literal = literal.lower()
        self.category = category
        self.direction = direction
        self.max_distance = max_distance  # Maximum distance in words


class NegationAssertionAnnotator(Annotator):
    """Clinical negation and assertion detection using pyConText-style rules."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.context_cues = self._load_default_cues()
        self.custom_cues = self.get_config("custom_cues", [])
        self.max_scope = self.get_config("max_scope", 10)  # words
        
        # Add custom cues
        for cue_config in self.custom_cues:
            cue = ContextCue(
                literal=cue_config["literal"],
                category=cue_config["category"],
                direction=ContextDirection(cue_config.get("direction", "bidirectional")),
                max_distance=cue_config.get("max_distance", 10)
            )
            self.context_cues.append(cue)
    
    def _load_default_cues(self) -> List[ContextCue]:
        """Load default context cues."""
        cues = []
        
        # Negation cues
        negation_literals = [
            "no", "not", "denies", "denied", "negative", "negative for",
            "without", "absent", "free of", "ruled out", "rules out",
            "no evidence of", "no signs of", "no symptoms of",
            "unremarkable", "within normal limits", "wnl",
            "non-contributory", "non-significant", "insignificant",
            "never", "none", "neither", "nor", "nothing",
            "refuses", "declines", "declined", "unable to", "cannot",
            "fails to", "failed to", "no complaints of", "no history of",
            "no known", "nk", "nka", "nkda"
        ]
        
        for literal in negation_literals:
            cues.append(ContextCue(
                literal=literal,
                category="negation",
                direction=ContextDirection.FORWARD,
                max_distance=6
            ))
        
        # Backward negation cues
        backward_negation = [
            "is ruled out", "was ruled out", "are ruled out", "were ruled out",
            "is negative", "was negative", "are negative", "were negative",
            "is absent", "was absent", "are absent", "were absent",
            "is unlikely", "was unlikely", "are unlikely", "were unlikely"
        ]
        
        for literal in backward_negation:
            cues.append(ContextCue(
                literal=literal,
                category="negation",
                direction=ContextDirection.BACKWARD,
                max_distance=3
            ))
        
        # Uncertainty/Possible cues
        uncertainty_literals = [
            "possible", "possibly", "probable", "probably", "likely",
            "may be", "might be", "could be", "suggest", "suggests",
            "suggestive of", "consistent with", "compatible with",
            "suspicious for", "suspect", "suspected", "questionable",
            "unclear", "uncertain", "undetermined", "rule out",
            "consider", "considering", "differential", "appears",
            "seems", "looks like", "impression of"
        ]
        
        for literal in uncertainty_literals:
            cues.append(ContextCue(
                literal=literal,
                category="uncertainty",
                direction=ContextDirection.FORWARD,
                max_distance=5
            ))
        
        # Family history cues
        family_literals = [
            "family history", "family hx", "fh", "familial", "hereditary",
            "mother", "father", "parent", "parents", "sibling", "sister",
            "brother", "grandmother", "grandfather", "grandparent",
            "grandparents", "aunt", "uncle", "cousin", "maternal",
            "paternal", "runs in family", "family history of"
        ]
        
        for literal in family_literals:
            cues.append(ContextCue(
                literal=literal,
                category="family_history",
                direction=ContextDirection.FORWARD,
                max_distance=8
            ))
        
        # Historical cues
        historical_literals = [
            "history of", "hx of", "h/o", "past", "previous", "prior",
            "previously", "former", "old", "remote", "distant",
            "years ago", "months ago", "weeks ago", "days ago",
            "in the past", "historically", "chronic", "longstanding",
            "long-standing", "since", "status post", "s/p"
        ]
        
        for literal in historical_literals:
            cues.append(ContextCue(
                literal=literal,
                category="historical",
                direction=ContextDirection.FORWARD,
                max_distance=6
            ))
        
        # Hypothetical/Conditional cues
        hypothetical_literals = [
            "if", "when", "unless", "should", "would", "could",
            "in case of", "in the event of", "prophylaxis",
            "prophylactic", "preventive", "prevention", "to prevent",
            "avoid", "risk of", "risk for", "predisposed to"
        ]
        
        for literal in hypothetical_literals:
            cues.append(ContextCue(
                literal=literal,
                category="hypothetical",
                direction=ContextDirection.FORWARD,
                max_distance=5
            ))
        
        return cues
    
    def initialize(self):
        """Initialize the assertion annotator."""
        # Create lookup dictionary for fast matching
        self.cue_lookup = {}
        for cue in self.context_cues:
            words = cue.literal.split()
            if len(words) == 1:
                if words[0] not in self.cue_lookup:
                    self.cue_lookup[words[0]] = []
                self.cue_lookup[words[0]].append(cue)
            else:
                # For multi-word cues, index by first word
                if words[0] not in self.cue_lookup:
                    self.cue_lookup[words[0]] = []
                self.cue_lookup[words[0]].append(cue)
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Apply assertion detection to named entities in the document."""
        # Get existing named entities
        entities = document.get_annotations(AnnotationType.NAMED_ENTITY)
        
        if not entities:
            return []
        
        # Tokenize document for context analysis
        words, word_positions = self._tokenize_with_positions(document.text)
        
        # Find context cues
        cue_matches = self._find_context_cues(words, word_positions)
        
        # Apply context to entities
        modified_entities = []
        
        for entity in entities:
            if isinstance(entity, NamedEntityAnnotation):
                # Find entity position in word list
                entity_word_indices = self._find_entity_word_indices(entity, words, word_positions)
                
                # Apply context rules
                assertion = self._determine_assertion(entity_word_indices, cue_matches, words)
                
                # Create new entity with assertion
                new_entity = NamedEntityAnnotation(
                    span=entity.span,
                    text=entity.text,
                    annotation_type=entity.annotation_type,
                    entity_type=entity.entity_type,
                    entity_subtype=entity.entity_subtype,
                    confidence=entity.confidence * 0.95,  # Slight confidence reduction
                    metadata={
                        **entity.metadata,
                        "assertion": assertion.value,
                        "context_applied": True
                    }
                )
                
                # Update the assertion field if it exists
                if hasattr(new_entity, 'assertion'):
                    new_entity.assertion = assertion
                
                modified_entities.append(new_entity)
            else:
                # Keep non-named entities unchanged
                modified_entities.append(entity)
        
        return modified_entities
    
    def _tokenize_with_positions(self, text: str) -> Tuple[List[str], List[Tuple[int, int]]]:
        """Tokenize text and return word positions."""
        words = []
        positions = []
        
        for match in re.finditer(r'\b\w+\b', text.lower()):
            words.append(match.group())
            positions.append((match.start(), match.end()))
        
        return words, positions
    
    def _find_context_cues(self, words: List[str], positions: List[Tuple[int, int]]) -> List[Dict]:
        """Find context cues in the word list."""
        cue_matches = []
        
        for i, word in enumerate(words):
            if word in self.cue_lookup:
                for cue in self.cue_lookup[word]:
                    # Check if this is a multi-word cue
                    cue_words = cue.literal.split()
                    if len(cue_words) == 1:
                        # Single word cue
                        cue_matches.append({
                            'cue': cue,
                            'start_word': i,
                            'end_word': i,
                            'start_char': positions[i][0],
                            'end_char': positions[i][1]
                        })
                    else:
                        # Multi-word cue - check if following words match
                        if i + len(cue_words) <= len(words):
                            match = True
                            for j, cue_word in enumerate(cue_words):
                                if words[i + j] != cue_word:
                                    match = False
                                    break
                            
                            if match:
                                cue_matches.append({
                                    'cue': cue,
                                    'start_word': i,
                                    'end_word': i + len(cue_words) - 1,
                                    'start_char': positions[i][0],
                                    'end_char': positions[i + len(cue_words) - 1][1]
                                })
        
        return cue_matches
    
    def _find_entity_word_indices(self, entity: Annotation, words: List[str], positions: List[Tuple[int, int]]) -> List[int]:
        """Find word indices that overlap with entity span."""
        entity_indices = []
        
        for i, (start, end) in enumerate(positions):
            if (start >= entity.start and start < entity.end) or \
               (end > entity.start and end <= entity.end) or \
               (start <= entity.start and end >= entity.end):
                entity_indices.append(i)
        
        return entity_indices
    
    def _determine_assertion(self, entity_word_indices: List[int], cue_matches: List[Dict], words: List[str]) -> AssertionType:
        """Determine assertion type based on context cues."""
        if not entity_word_indices:
            return AssertionType.PRESENT
        
        entity_start = min(entity_word_indices)
        entity_end = max(entity_word_indices)
        
        # Check each cue for applicability
        applicable_cues = []
        
        for cue_match in cue_matches:
            cue = cue_match['cue']
            cue_start = cue_match['start_word']
            cue_end = cue_match['end_word']
            
            # Check if cue is within scope and direction
            distance = float('inf')
            applies = False
            
            if cue.direction == ContextDirection.FORWARD:
                # Cue should be before entity
                if cue_end < entity_start:
                    distance = entity_start - cue_end
                    applies = distance <= cue.max_distance
            elif cue.direction == ContextDirection.BACKWARD:
                # Cue should be after entity
                if cue_start > entity_end:
                    distance = cue_start - entity_end
                    applies = distance <= cue.max_distance
            else:  # BIDIRECTIONAL
                # Cue can be before or after
                if cue_end < entity_start:
                    distance = entity_start - cue_end
                elif cue_start > entity_end:
                    distance = cue_start - entity_end
                else:
                    distance = 0  # Overlapping
                applies = distance <= cue.max_distance
            
            if applies:
                applicable_cues.append((cue, distance))
        
        # Sort by distance (closest first)
        applicable_cues.sort(key=lambda x: x[1])
        
        # Apply cues in order of precedence
        for cue, distance in applicable_cues:
            if cue.category == "negation":
                return AssertionType.ABSENT
            elif cue.category == "uncertainty":
                return AssertionType.POSSIBLE
            elif cue.category == "family_history":
                return AssertionType.FAMILY_HISTORY
            elif cue.category == "historical":
                return AssertionType.HISTORICAL
            elif cue.category == "hypothetical":
                return AssertionType.HYPOTHETICAL
        
        return AssertionType.PRESENT
    
    def process_entities(self, document: Document, entities: List[NamedEntityAnnotation]) -> List[NamedEntityAnnotation]:
        """Process a list of entities and return them with assertion labels."""
        # Create temporary document with entities
        temp_doc = Document(text=document.text, annotations=entities)
        
        # Apply assertion detection
        processed_entities = self.annotate(temp_doc)
        
        return [e for e in processed_entities if isinstance(e, NamedEntityAnnotation)]
