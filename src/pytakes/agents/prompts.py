"""
LLM Agent Prompt Templates for PyTAKES

This module defines prompt templates and schemas for the agentic LLM layer
that provides intelligent disambiguation and active learning capabilities.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class PromptType(Enum):
    """Types of prompts used in the LLM agent system."""
    CONCEPT_DISAMBIGUATION = "concept_disambiguation"
    ASSERTION_CLARIFICATION = "assertion_clarification"
    RELATION_EXTRACTION = "relation_extraction"
    SECTION_DETECTION = "section_detection"
    QUALITY_ASSESSMENT = "quality_assessment"


class ConfidenceLevel(Enum):
    """Confidence levels for triggering LLM intervention."""
    HIGH = "high"          # > 0.9
    MEDIUM = "medium"      # 0.7 - 0.9
    LOW = "low"           # 0.5 - 0.7
    VERY_LOW = "very_low" # < 0.5


class PromptTemplate(BaseModel):
    """Base class for LLM prompt templates."""
    
    prompt_type: PromptType
    template: str
    required_context: List[str] = Field(default_factory=list)
    confidence_threshold: float = 0.7
    max_tokens: int = 500
    temperature: float = 0.1
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConceptDisambiguationPrompt(PromptTemplate):
    """Prompt for disambiguating clinical concepts with low confidence."""
    
    template: str = """
You are a clinical NLP expert helping to disambiguate medical concepts.

CONTEXT:
- Clinical Text: "{clinical_text}"
- Identified Span: "{span_text}" (positions {start}-{end})
- Candidate Concepts: {candidate_concepts}
- Current Top Prediction: {top_prediction} (confidence: {confidence:.2f})

TASK:
Based on the clinical context, determine the most appropriate UMLS concept for the span "{span_text}".

ONTOLOGY CONSTRAINTS:
- Must map to SNOMED CT, RxNorm, or LOINC
- Consider semantic type restrictions: {semantic_types}
- Respect vocabulary preferences: {vocabulary_preferences}

REASONING:
1. Analyze the clinical context around "{span_text}"
2. Consider the semantic meaning in this specific context
3. Evaluate each candidate concept for appropriateness
4. Provide your reasoning for the final selection

RESPONSE FORMAT:
{{
    "selected_concept": {{
        "cui": "C1234567",
        "preferred_name": "Concept Name",
        "semantic_type": "T047",
        "vocabulary": "SNOMEDCT_US"
    }},
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this concept was selected",
    "alternative_concepts": [
        {{"cui": "C7654321", "reason": "Why this was not selected"}}
    ]
}}
"""

    prompt_type: PromptType = PromptType.CONCEPT_DISAMBIGUATION
    required_context: List[str] = Field(default_factory=lambda: [
        "clinical_text", "span_text", "start", "end", 
        "candidate_concepts", "top_prediction", "confidence"
    ])


class AssertionClarificationPrompt(PromptTemplate):
    """Prompt for clarifying assertion status (present/absent/possible/etc.)."""
    
    template: str = """
You are a clinical NLP expert analyzing assertion status for medical concepts.

CONTEXT:
- Clinical Text: "{clinical_text}"
- Medical Concept: "{concept_text}" (positions {start}-{end})
- UMLS Concept: {concept_name} ({cui})
- Current Assertion: {current_assertion} (confidence: {confidence:.2f})

TASK:
Determine the correct assertion status for "{concept_text}" in this clinical context.

ASSERTION CATEGORIES:
- PRESENT: The condition/finding is currently present
- ABSENT: Explicitly denied or ruled out
- POSSIBLE: Uncertain, possible, or suspected
- CONDITIONAL: Depends on circumstances ("if", "when")
- HYPOTHETICAL: Not actual ("rule out", "consider")
- FAMILY_HISTORY: Refers to family member
- HISTORICAL: Past condition, no longer present

CONTEXT CLUES:
- Negation indicators: {negation_patterns}
- Uncertainty markers: {uncertainty_patterns}
- Temporal indicators: {temporal_patterns}
- Experiencer markers: {experiencer_patterns}

RESPONSE FORMAT:
{{
    "assertion_status": "PRESENT|ABSENT|POSSIBLE|CONDITIONAL|HYPOTHETICAL|FAMILY_HISTORY|HISTORICAL",
    "confidence": 0.95,
    "supporting_evidence": ["specific phrases or context that support this assertion"],
    "reasoning": "Brief explanation of the assertion determination"
}}
"""

    prompt_type: PromptType = PromptType.ASSERTION_CLARIFICATION
    required_context: List[str] = Field(default_factory=lambda: [
        "clinical_text", "concept_text", "start", "end",
        "concept_name", "cui", "current_assertion", "confidence"
    ])


class RelationExtractionPrompt(PromptTemplate):
    """Prompt for extracting relations between clinical entities."""
    
    template: str = """
You are a clinical NLP expert identifying relationships between medical entities.

CONTEXT:
- Clinical Text: "{clinical_text}"
- Entity 1: "{entity1_text}" ({entity1_type}) at positions {entity1_start}-{entity1_end}
- Entity 2: "{entity2_text}" ({entity2_type}) at positions {entity2_start}-{entity2_end}

TASK:
Identify if there is a clinically meaningful relationship between these entities.

RELATION TYPES:
- MEDICATION_DOSAGE: Medication and its dosage/frequency
- MEDICATION_INDICATION: Medication and the condition it treats
- TEMPORAL: Entity and time expression ("since 2015", "for 3 months")
- CAUSALITY: Cause and effect relationships
- MANIFESTATION: Condition and its symptoms/findings
- LOCATION: Anatomical location relationships
- SEVERITY: Condition and severity descriptors
- EXPERIENCER: Who experiences the condition (patient, family member)

RESPONSE FORMAT:
{{
    "relation_exists": true,
    "relation_type": "MEDICATION_DOSAGE",
    "direction": "entity1_to_entity2|entity2_to_entity1|bidirectional",
    "confidence": 0.90,
    "supporting_text": "specific text span that indicates the relation",
    "reasoning": "Why this relation was identified"
}}

If no relation exists, return:
{{
    "relation_exists": false,
    "reasoning": "Why no relation was found"
}}
"""

    prompt_type: PromptType = PromptType.RELATION_EXTRACTION
    required_context: List[str] = Field(default_factory=lambda: [
        "clinical_text", "entity1_text", "entity1_type", "entity1_start", "entity1_end",
        "entity2_text", "entity2_type", "entity2_start", "entity2_end"
    ])


class QualityAssessmentPrompt(PromptTemplate):
    """Prompt for assessing the quality of annotations and suggesting improvements."""
    
    template: str = """
You are a clinical NLP quality assurance expert reviewing annotation accuracy.

CONTEXT:
- Clinical Text: "{clinical_text}"
- Current Annotations: {current_annotations}
- Annotation Confidence Scores: {confidence_scores}
- Domain: {clinical_domain}

TASK:
Assess the quality of the current annotations and identify potential issues.

QUALITY CRITERIA:
1. COMPLETENESS: Are all relevant medical entities identified?
2. ACCURACY: Are the concepts correctly mapped to UMLS?
3. CONSISTENCY: Are similar entities annotated consistently?
4. PRECISION: Are the span boundaries accurate?
5. CLINICAL_RELEVANCE: Are the annotations clinically meaningful?

COMMON ISSUES:
- Missing entities (false negatives)
- Incorrect concept mappings
- Wrong assertion status
- Overlapping or conflicting annotations
- Inappropriate span boundaries

RESPONSE FORMAT:
{{
    "overall_quality_score": 0.85,
    "issues_identified": [
        {{
            "issue_type": "MISSING_ENTITY",
            "description": "Potential medication 'aspirin' not annotated",
            "suggested_span": {{"start": 45, "end": 52}},
            "confidence": 0.8
        }}
    ],
    "suggested_improvements": [
        "Add negation detection for 'no chest pain'",
        "Consider family history context for 'mother had diabetes'"
    ],
    "confidence_in_assessment": 0.9
}}
"""

    prompt_type: PromptType = PromptType.QUALITY_ASSESSMENT
    required_context: List[str] = Field(default_factory=lambda: [
        "clinical_text", "current_annotations", "confidence_scores"
    ])


class ActiveLearningFeedback(BaseModel):
    """Schema for active learning feedback collection."""
    
    document_id: str
    annotation_id: str
    user_id: str
    feedback_type: str  # "correction", "confirmation", "rejection"
    original_annotation: Dict[str, Any]
    corrected_annotation: Optional[Dict[str, Any]] = None
    user_comments: Optional[str] = None
    confidence_before: float
    confidence_after: Optional[float] = None
    timestamp: str
    clinical_context: Optional[str] = None


class LLMAgentConfig(BaseModel):
    """Configuration for the LLM agent system."""
    
    model_name: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    confidence_thresholds: Dict[PromptType, float] = Field(default_factory=lambda: {
        PromptType.CONCEPT_DISAMBIGUATION: 0.7,
        PromptType.ASSERTION_CLARIFICATION: 0.6,
        PromptType.RELATION_EXTRACTION: 0.8,
        PromptType.SECTION_DETECTION: 0.5,
        PromptType.QUALITY_ASSESSMENT: 0.0  # Always run for quality checks
    })
    max_tokens: int = 1000
    temperature: float = 0.1
    timeout: int = 30
    retry_attempts: int = 3
    enable_caching: bool = True
    cache_ttl: int = 3600  # seconds


# Prompt registry
PROMPT_REGISTRY: Dict[PromptType, PromptTemplate] = {
    PromptType.CONCEPT_DISAMBIGUATION: ConceptDisambiguationPrompt(),
    PromptType.ASSERTION_CLARIFICATION: AssertionClarificationPrompt(),
    PromptType.RELATION_EXTRACTION: RelationExtractionPrompt(),
    PromptType.QUALITY_ASSESSMENT: QualityAssessmentPrompt(),
}


def get_prompt_template(prompt_type: PromptType) -> PromptTemplate:
    """Get a prompt template by type."""
    return PROMPT_REGISTRY.get(prompt_type)


def should_trigger_llm(confidence: float, prompt_type: PromptType, config: LLMAgentConfig) -> bool:
    """Determine if LLM intervention should be triggered based on confidence."""
    threshold = config.confidence_thresholds.get(prompt_type, 0.7)
    return confidence < threshold
