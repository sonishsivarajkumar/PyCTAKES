"""Clinical section detection annotator."""

import re
from typing import List, Dict, Optional, Tuple

from ..types import Document, Annotation, Span, AnnotationType, SectionAnnotation
from .base import Annotator


class ClinicalSectionDetector(Annotator):
    """Detect clinical sections in medical documents."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.section_patterns = self._load_default_patterns()
        self.custom_patterns = self.get_config("custom_patterns", {})
        self.case_sensitive = self.get_config("case_sensitive", False)
        
        # Merge custom patterns with defaults
        self.section_patterns.update(self.custom_patterns)
    
    def _load_default_patterns(self) -> Dict[str, List[str]]:
        """Load default clinical section patterns."""
        return {
            "chief_complaint": [
                r"chief\s+complaint",
                r"cc:",
                r"c/c:",
                r"presenting\s+complaint",
                r"reason\s+for\s+visit"
            ],
            "history_present_illness": [
                r"history\s+of\s+present\s+illness",
                r"hpi:",
                r"h\.?p\.?i\.?:",
                r"present\s+illness",
                r"history\s+of\s+presenting\s+complaint"
            ],
            "past_medical_history": [
                r"past\s+medical\s+history",
                r"pmh:",
                r"p\.?m\.?h\.?:",
                r"medical\s+history",
                r"past\s+history",
                r"previous\s+medical\s+history"
            ],
            "medications": [
                r"medications?",
                r"meds:",
                r"current\s+medications?",
                r"home\s+medications?",
                r"drug\s+list",
                r"prescription\s+medications?"
            ],
            "allergies": [
                r"allergies",
                r"allergy",
                r"drug\s+allergies",
                r"medication\s+allergies",
                r"known\s+allergies",
                r"nka", # no known allergies
                r"nkda" # no known drug allergies
            ],
            "social_history": [
                r"social\s+history",
                r"sh:",
                r"s\.?h\.?:",
                r"social\s+hx",
                r"lifestyle"
            ],
            "family_history": [
                r"family\s+history",
                r"fh:",
                r"f\.?h\.?:",
                r"family\s+hx",
                r"familial\s+history"
            ],
            "review_of_systems": [
                r"review\s+of\s+systems?",
                r"ros:",
                r"r\.?o\.?s\.?:",
                r"systems?\s+review",
                r"symptom\s+review"
            ],
            "physical_exam": [
                r"physical\s+exam(?:ination)?",
                r"pe:",
                r"p\.?e\.?:",
                r"exam(?:ination)?",
                r"physical\s+findings",
                r"objective\s+findings"
            ],
            "vital_signs": [
                r"vital\s+signs?",
                r"vitals?",
                r"vs:",
                r"v\.?s\.?:",
                r"temperature",
                r"blood\s+pressure",
                r"heart\s+rate",
                r"respiratory\s+rate"
            ],
            "laboratory": [
                r"laboratory\s+(?:results?|data|findings?)",
                r"labs?:",
                r"lab\s+(?:results?|data|findings?)",
                r"laboratory\s+studies",
                r"diagnostic\s+tests?"
            ],
            "radiology": [
                r"radiology",
                r"imaging",
                r"x-ray",
                r"ct\s+scan",
                r"mri",
                r"ultrasound",
                r"radiologic\s+studies"
            ],
            "assessment": [
                r"assessment",
                r"impression",
                r"diagnosis",
                r"clinical\s+impression",
                r"diagnostic\s+impression"
            ],
            "plan": [
                r"plan",
                r"treatment\s+plan",
                r"management\s+plan",
                r"therapeutic\s+plan",
                r"recommendations?"
            ],
            "assessment_and_plan": [
                r"assessment\s+and\s+plan",
                r"a&p:",
                r"a\s*&\s*p:",
                r"impression\s+and\s+plan"
            ],
            "discharge_summary": [
                r"discharge\s+summary",
                r"discharge\s+note",
                r"hospital\s+course",
                r"summary"
            ],
            "procedures": [
                r"procedures?",
                r"surgical\s+procedures?",
                r"interventions?",
                r"operations?"
            ]
        }
    
    def initialize(self):
        """Initialize the section detector."""
        # Compile regex patterns for efficiency
        self.compiled_patterns = {}
        flags = 0 if self.case_sensitive else re.IGNORECASE
        
        for section_type, patterns in self.section_patterns.items():
            compiled = []
            for pattern in patterns:
                # Add word boundaries and optional punctuation/whitespace
                enhanced_pattern = rf"\b{pattern}\b\s*:?\s*"
                compiled.append(re.compile(enhanced_pattern, flags))
            self.compiled_patterns[section_type] = compiled
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Detect clinical sections in the document."""
        text = document.text
        sections = []
        
        # Find all section headers
        section_boundaries = []
        
        for section_type, pattern_list in self.compiled_patterns.items():
            for pattern in pattern_list:
                for match in pattern.finditer(text):
                    section_boundaries.append({
                        'start': match.start(),
                        'end': match.end(),
                        'type': section_type,
                        'header_text': match.group().strip(),
                        'confidence': self._calculate_confidence(match.group(), section_type)
                    })
        
        # Sort by position
        section_boundaries.sort(key=lambda x: x['start'])
        
        # Create section annotations with content
        for i, boundary in enumerate(section_boundaries):
            # Determine section content end
            if i + 1 < len(section_boundaries):
                content_end = section_boundaries[i + 1]['start']
            else:
                content_end = len(text)
            
            # Extract section content (skip header)
            header_end = boundary['end']
            section_content = text[header_end:content_end].strip()
            
            # Create section span including header and content
            section_span = Span(start=boundary['start'], end=content_end)
            full_text = text[boundary['start']:content_end].strip()
            
            section = SectionAnnotation(
                span=section_span,
                text=full_text,
                annotation_type=AnnotationType.SECTION,
                section_type=boundary['type'],
                confidence=boundary['confidence'],
                metadata={
                    'header_text': boundary['header_text'],
                    'content': section_content,
                    'header_span': {'start': boundary['start'], 'end': boundary['end']}
                }
            )
            sections.append(section)
        
        return sections
    
    def _calculate_confidence(self, matched_text: str, section_type: str) -> float:
        """Calculate confidence score for section detection."""
        base_confidence = 0.85
        
        # Boost confidence for exact matches
        clean_text = matched_text.lower().strip().rstrip(':').strip()
        
        exact_matches = {
            'chief_complaint': ['chief complaint', 'cc'],
            'history_present_illness': ['history of present illness', 'hpi'],
            'past_medical_history': ['past medical history', 'pmh', 'medical history'],
            'medications': ['medications', 'meds'],
            'allergies': ['allergies', 'allergy'],
            'social_history': ['social history', 'sh'],
            'family_history': ['family history', 'fh'],
            'review_of_systems': ['review of systems', 'ros'],
            'physical_exam': ['physical exam', 'physical examination', 'pe'],
            'vital_signs': ['vital signs', 'vitals', 'vs'],
            'laboratory': ['laboratory', 'labs', 'lab results'],
            'radiology': ['radiology', 'imaging'],
            'assessment': ['assessment', 'impression'],
            'plan': ['plan'],
            'assessment_and_plan': ['assessment and plan', 'a&p'],
            'procedures': ['procedures', 'procedure']
        }
        
        if section_type in exact_matches:
            if clean_text in exact_matches[section_type]:
                return min(0.98, base_confidence + 0.10)
        
        # Adjust based on text length and format
        if ':' in matched_text:
            base_confidence += 0.05
        
        if len(clean_text) <= 3:  # Short abbreviations
            base_confidence += 0.05
        
        return min(0.95, base_confidence)
    
    def get_section_content(self, document: Document, section_type: str) -> Optional[str]:
        """Extract content for a specific section type."""
        # Find sections in document
        sections = self.annotate(document)
        
        for section in sections:
            if hasattr(section, 'section_type') and section.section_type == section_type:
                return section.metadata.get('content', '')
        
        return None
    
    def get_all_sections(self, document: Document) -> Dict[str, str]:
        """Get all detected sections as a dictionary."""
        sections = self.annotate(document)
        result = {}
        
        for section in sections:
            if hasattr(section, 'section_type'):
                section_type = section.section_type
                content = section.metadata.get('content', '')
                
                # Handle multiple sections of same type
                if section_type in result:
                    result[section_type] += "\n\n" + content
                else:
                    result[section_type] = content
        
        return result
