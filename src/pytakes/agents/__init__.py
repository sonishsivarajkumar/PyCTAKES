"""Agents package for PyTAKES LLM integration."""

from .prompts import (
    PromptType,
    PromptTemplate,
    ConceptDisambiguationPrompt,
    AssertionClarificationPrompt,
    RelationExtractionPrompt,
    QualityAssessmentPrompt,
    ActiveLearningFeedback,
    LLMAgentConfig,
    get_prompt_template,
    should_trigger_llm,
)

__all__ = [
    "PromptType",
    "PromptTemplate", 
    "ConceptDisambiguationPrompt",
    "AssertionClarificationPrompt",
    "RelationExtractionPrompt", 
    "QualityAssessmentPrompt",
    "ActiveLearningFeedback",
    "LLMAgentConfig",
    "get_prompt_template",
    "should_trigger_llm",
]
