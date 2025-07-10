# Custom Annotators

Learn how to create and integrate custom annotators into the pyCTAKES pipeline.

## Overview

pyCTAKES provides a flexible architecture for creating custom annotators that can be seamlessly integrated into processing pipelines. Custom annotators allow you to:

- Implement domain-specific processing logic
- Integrate external NLP models or services
- Add proprietary algorithms or rules
- Extend functionality for specific use cases

## Base Annotator Interface

All annotators must extend the `BaseAnnotator` class:

```python
from pyctakes.annotators.base import BaseAnnotator
from pyctakes.types import Document

class CustomAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        # Initialize your annotator
        
    def process(self, doc: Document) -> Document:
        # Your processing logic here
        return doc
```

## Simple Custom Annotator Example

Here's a basic custom annotator that identifies phone numbers:

```python
import re
from pyctakes.annotators.base import BaseAnnotator
from pyctakes.types import Document, Entity

class PhoneNumberAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        self.phone_pattern = re.compile(
            r'\b(?:\+?1[-.\s]?)?'
            r'\(?([0-9]{3})\)?[-.\s]?'
            r'([0-9]{3})[-.\s]?'
            r'([0-9]{4})\b'
        )
    
    def process(self, doc: Document) -> Document:
        # Find phone numbers in text
        for match in self.phone_pattern.finditer(doc.text):
            entity = Entity(
                start=match.start(),
                end=match.end(),
                text=match.group(),
                label="PHONE_NUMBER",
                confidence=1.0
            )
            doc.entities.append(entity)
        
        return doc
```

## Advanced Custom Annotator

Here's a more sophisticated annotator that integrates with an external API:

```python
import requests
from typing import Dict, Any
from pyctakes.annotators.base import BaseAnnotator
from pyctakes.types import Document, Entity, UMLSConcept

class ExternalNERAnnotator(BaseAnnotator):
    def __init__(self, api_url: str, api_key: str, **kwargs):
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.config = kwargs
    
    def process(self, doc: Document) -> Document:
        try:
            # Call external NER API
            response = self._call_api(doc.text)
            
            # Process API response
            entities = self._parse_response(response)
            
            # Add entities to document
            doc.entities.extend(entities)
            
        except Exception as e:
            self.logger.error(f"External API failed: {e}")
            # Optionally fall back to rule-based approach
            
        return doc
    
    def _call_api(self, text: str) -> Dict[str, Any]:
        payload = {
            "text": text,
            "options": self.config
        }
        response = requests.post(
            self.api_url,
            json=payload,
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, response: Dict[str, Any]) -> List[Entity]:
        entities = []
        for item in response.get("entities", []):
            entity = Entity(
                start=item["start"],
                end=item["end"],
                text=item["text"],
                label=item["label"],
                confidence=item.get("confidence", 1.0)
            )
            
            # Add UMLS concept if available
            if "concept" in item:
                entity.umls_concept = UMLSConcept(
                    cui=item["concept"]["cui"],
                    preferred_term=item["concept"]["name"],
                    confidence=item["concept"]["score"]
                )
            
            entities.append(entity)
        
        return entities
```

## Configuration Support

Add configuration support to your custom annotators:

```python
from pyctakes.annotators.base import BaseAnnotator

class ConfigurableAnnotator(BaseAnnotator):
    def __init__(self, config: Dict[str, Any] = None, **kwargs):
        super().__init__()
        
        # Default configuration
        self.config = {
            "case_sensitive": False,
            "min_confidence": 0.5,
            "max_entities": 100,
            "custom_patterns": {}
        }
        
        # Update with provided config
        if config:
            self.config.update(config)
        
        # Update with keyword arguments
        self.config.update(kwargs)
        
        # Initialize with configuration
        self._initialize()
    
    def _initialize(self):
        # Setup based on configuration
        self.case_sensitive = self.config["case_sensitive"]
        self.min_confidence = self.config["min_confidence"]
        # ... other initialization
```

## Error Handling

Implement robust error handling in your annotators:

```python
from pyctakes.annotators.base import BaseAnnotator, AnnotationError

class RobustAnnotator(BaseAnnotator):
    def process(self, doc: Document) -> Document:
        try:
            return self._process_safely(doc)
        
        except Exception as e:
            self.logger.error(f"Annotation failed: {e}")
            
            # Option 1: Re-raise as AnnotationError
            raise AnnotationError(f"RobustAnnotator failed: {e}")
            
            # Option 2: Return document unchanged
            # return doc
            
            # Option 3: Apply fallback processing
            # return self._fallback_process(doc)
    
    def _process_safely(self, doc: Document) -> Document:
        # Your main processing logic
        pass
    
    def _fallback_process(self, doc: Document) -> Document:
        # Simplified fallback processing
        pass
```

## Multi-language Support

Create annotators that support multiple languages:

```python
from pyctakes.annotators.base import BaseAnnotator

class MultilingualAnnotator(BaseAnnotator):
    def __init__(self, language: str = "en", **kwargs):
        super().__init__()
        self.language = language
        self.patterns = self._load_patterns(language)
    
    def _load_patterns(self, language: str) -> Dict[str, List[str]]:
        patterns = {
            "en": {
                "MEDICATION": ["aspirin", "ibuprofen"],
                "CONDITION": ["diabetes", "hypertension"]
            },
            "es": {
                "MEDICATION": ["aspirina", "ibuprofeno"],
                "CONDITION": ["diabetes", "hipertensión"]
            }
        }
        return patterns.get(language, patterns["en"])
    
    def process(self, doc: Document) -> Document:
        # Process using language-specific patterns
        for label, terms in self.patterns.items():
            doc = self._find_entities(doc, terms, label)
        return doc
```

## Performance Optimization

Optimize your annotators for better performance:

```python
from functools import lru_cache
from pyctakes.annotators.base import BaseAnnotator

class OptimizedAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        # Pre-compile patterns for better performance
        self.compiled_patterns = self._compile_patterns()
        
        # Cache for expensive operations
        self._cache = {}
    
    @lru_cache(maxsize=1000)
    def _expensive_operation(self, text: str) -> str:
        # Expensive computation cached with LRU
        pass
    
    def _compile_patterns(self):
        # Pre-compile regex patterns
        patterns = {}
        for label, pattern_list in self.raw_patterns.items():
            patterns[label] = [re.compile(p, re.IGNORECASE) 
                             for p in pattern_list]
        return patterns
    
    def process(self, doc: Document) -> Document:
        # Use compiled patterns for faster matching
        for label, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(doc.text):
                    # Process match
                    pass
        
        return doc
```

## Testing Custom Annotators

Create comprehensive tests for your custom annotators:

```python
import pytest
from pyctakes.types import Document
from your_module import CustomAnnotator

class TestCustomAnnotator:
    def setup_method(self):
        self.annotator = CustomAnnotator()
    
    def test_basic_functionality(self):
        doc = Document(text="Test input text")
        result = self.annotator.process(doc)
        
        assert len(result.entities) > 0
        assert result.entities[0].label == "EXPECTED_LABEL"
    
    def test_empty_input(self):
        doc = Document(text="")
        result = self.annotator.process(doc)
        
        assert len(result.entities) == 0
    
    def test_configuration(self):
        annotator = CustomAnnotator(custom_param="value")
        doc = Document(text="Test text")
        result = annotator.process(doc)
        
        # Test configuration effects
        assert result is not None
    
    def test_error_handling(self):
        # Test that annotator handles errors gracefully
        doc = Document(text="Text that might cause errors")
        
        # Should not raise exception
        result = self.annotator.process(doc)
        assert result is not None
```

## Integration with Pipeline

Register your custom annotator for use in pipelines:

```python
from pyctakes.pipeline import Pipeline

# Method 1: Direct addition
pipeline = Pipeline()
pipeline.add_annotator(CustomAnnotator())

# Method 2: Configuration-based
config = {
    "annotators": [
        {
            "name": "custom",
            "class": "your_module.CustomAnnotator",
            "config": {
                "param1": "value1"
            }
        }
    ]
}
pipeline = Pipeline.from_config(config)
```

## Plugin Architecture

Create installable plugins for your annotators:

```python
# setup.py
from setuptools import setup

setup(
    name="pyctakes-custom-plugin",
    version="1.0.0",
    packages=["pyctakes_custom"],
    entry_points={
        "pyctakes.annotators": [
            "custom = pyctakes_custom:CustomAnnotator"
        ]
    }
)
```

## Best Practices

1. **Follow naming conventions**: Use descriptive class names ending in "Annotator"
2. **Document thoroughly**: Include docstrings and type hints
3. **Handle errors gracefully**: Don't let your annotator crash the pipeline
4. **Make it configurable**: Support configuration for flexibility
5. **Test extensively**: Unit tests and integration tests
6. **Optimize for performance**: Profile and optimize bottlenecks
7. **Support standard types**: Use pyCTAKES type system correctly
8. **Log appropriately**: Use logging for debugging and monitoring

## Example: Complete Custom Annotator

Here's a complete example of a well-structured custom annotator:

```python
"""
Custom vital signs annotator for pyCTAKES.
"""
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from pyctakes.annotators.base import BaseAnnotator
from pyctakes.types import Document, Entity

@dataclass
class VitalSign:
    name: str
    value: float
    unit: str
    normal_range: tuple

class VitalSignsAnnotator(BaseAnnotator):
    """
    Annotator for extracting vital signs from clinical text.
    
    Recognizes common vital signs like blood pressure, heart rate,
    temperature, respiratory rate, and oxygen saturation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__()
        
        self.config = {
            "include_normal_ranges": True,
            "min_confidence": 0.8,
            "custom_patterns": {}
        }
        
        if config:
            self.config.update(config)
        self.config.update(kwargs)
        
        self.logger = logging.getLogger(__name__)
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for vital signs recognition."""
        
        patterns = {
            "BLOOD_PRESSURE": [
                r'\b(?:BP|Blood Pressure):\s*(\d{2,3})/(\d{2,3})\s*(?:mmHg)?\b',
                r'\b(\d{2,3})/(\d{2,3})\s*mmHg\b'
            ],
            "HEART_RATE": [
                r'\b(?:HR|Heart Rate):\s*(\d{2,3})\s*(?:bpm)?\b',
                r'\bPulse:\s*(\d{2,3})\s*(?:bpm)?\b'
            ],
            "TEMPERATURE": [
                r'\b(?:Temp|Temperature):\s*(\d{2,3}(?:\.\d)?)\s*°?([CF])?\b',
                r'\b(\d{2,3}(?:\.\d)?)\s*°([CF])\b'
            ]
        }
        
        # Add custom patterns
        patterns.update(self.config.get("custom_patterns", {}))
        
        # Compile patterns
        self.compiled_patterns = {}
        for vital_type, pattern_list in patterns.items():
            self.compiled_patterns[vital_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in pattern_list
            ]
    
    def process(self, doc: Document) -> Document:
        """
        Process document to extract vital signs.
        
        Args:
            doc: Input document
            
        Returns:
            Document with vital signs entities added
        """
        try:
            for vital_type, patterns in self.compiled_patterns.items():
                entities = self._extract_vital_signs(doc.text, vital_type, patterns)
                doc.entities.extend(entities)
            
            self.logger.debug(f"Extracted {len(doc.entities)} vital signs")
            
        except Exception as e:
            self.logger.error(f"Vital signs extraction failed: {e}")
            
        return doc
    
    def _extract_vital_signs(self, text: str, vital_type: str, 
                           patterns: List[re.Pattern]) -> List[Entity]:
        """Extract specific type of vital signs from text."""
        
        entities = []
        
        for pattern in patterns:
            for match in pattern.finditer(text):
                entity = self._create_entity(match, vital_type)
                if entity and entity.confidence >= self.config["min_confidence"]:
                    entities.append(entity)
        
        return entities
    
    def _create_entity(self, match: re.Match, vital_type: str) -> Optional[Entity]:
        """Create entity from regex match."""
        
        try:
            vital_sign = self._parse_vital_sign(match, vital_type)
            confidence = self._calculate_confidence(vital_sign)
            
            entity = Entity(
                start=match.start(),
                end=match.end(),
                text=match.group(),
                label=vital_type,
                confidence=confidence
            )
            
            # Add structured data
            entity.vital_sign = vital_sign
            
            return entity
            
        except Exception as e:
            self.logger.warning(f"Failed to parse vital sign: {e}")
            return None
    
    def _parse_vital_sign(self, match: re.Match, vital_type: str) -> VitalSign:
        """Parse vital sign from regex match."""
        
        if vital_type == "BLOOD_PRESSURE":
            systolic = int(match.group(1))
            diastolic = int(match.group(2))
            return VitalSign(
                name="Blood Pressure",
                value=(systolic, diastolic),
                unit="mmHg",
                normal_range=(90, 140)
            )
        
        elif vital_type == "HEART_RATE":
            rate = int(match.group(1))
            return VitalSign(
                name="Heart Rate",
                value=rate,
                unit="bpm",
                normal_range=(60, 100)
            )
        
        # Add other vital signs...
        
        raise ValueError(f"Unknown vital type: {vital_type}")
    
    def _calculate_confidence(self, vital_sign: VitalSign) -> float:
        """Calculate confidence based on vital sign reasonableness."""
        
        # Simple heuristic: higher confidence for values in normal range
        base_confidence = 0.9
        
        if self._is_in_normal_range(vital_sign):
            return base_confidence
        else:
            return base_confidence * 0.8
    
    def _is_in_normal_range(self, vital_sign: VitalSign) -> bool:
        """Check if vital sign is in normal range."""
        
        if vital_sign.name == "Blood Pressure":
            systolic, diastolic = vital_sign.value
            return (90 <= systolic <= 140) and (60 <= diastolic <= 90)
        
        elif vital_sign.name == "Heart Rate":
            return 60 <= vital_sign.value <= 100
        
        return True  # Default to normal if unknown
```

This example demonstrates all the best practices for creating robust, configurable, and well-tested custom annotators for pyCTAKES.
