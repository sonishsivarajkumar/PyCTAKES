"""Clinical Named Entity Recognition annotators."""

import re
from typing import List, Dict, Optional, Set, Tuple

try:
    import spacy
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False

from ..types import (
    Document, Annotation, Span, AnnotationType, 
    NamedEntityAnnotation, EntityType
)
from .base import Annotator


class ClinicalNERAnnotator(Annotator):
    """Clinical Named Entity Recognition using rule-based and model-based approaches."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.use_model = self.get_config("use_model", True)
        self.model_name = self.get_config("model_name", "en_core_sci_sm")  # scispaCy model
        self.use_rules = self.get_config("use_rules", True)
        self.nlp = None
        
        # Initialize rule-based dictionaries
        self.entity_dictionaries = self._load_clinical_dictionaries()
    
    def _load_clinical_dictionaries(self) -> Dict[EntityType, Set[str]]:
        """Load clinical entity dictionaries."""
        return {
            EntityType.DISORDER: {
                # Common disorders
                "diabetes", "diabetes mellitus", "hypertension", "high blood pressure",
                "hyperlipidemia", "obesity", "depression", "anxiety", "asthma",
                "copd", "chronic obstructive pulmonary disease", "pneumonia",
                "myocardial infarction", "heart attack", "stroke", "cva",
                "cerebrovascular accident", "atrial fibrillation", "heart failure",
                "congestive heart failure", "chf", "angina", "chest pain",
                "shortness of breath", "dyspnea", "chronic kidney disease",
                "ckd", "renal failure", "kidney failure", "cirrhosis",
                "hepatitis", "gastroesophageal reflux", "gerd", "peptic ulcer",
                "inflammatory bowel disease", "ibd", "crohn's disease",
                "ulcerative colitis", "rheumatoid arthritis", "osteoarthritis",
                "osteoporosis", "fracture", "cancer", "carcinoma", "tumor",
                "neoplasm", "malignancy", "leukemia", "lymphoma", "melanoma",
                "alzheimer's disease", "dementia", "parkinson's disease",
                "multiple sclerosis", "epilepsy", "seizure", "migraine",
                "headache", "back pain", "arthritis", "fibromyalgia"
            },
            
            EntityType.MEDICATION: {
                # Common medications
                "metformin", "insulin", "lisinopril", "atorvastatin", "simvastatin",
                "amlodipine", "hydrochlorothiazide", "hctz", "losartan", "aspirin",
                "warfarin", "clopidogrel", "plavix", "omeprazole", "pantoprazole",
                "albuterol", "fluticasone", "prednisone", "ibuprofen", "acetaminophen",
                "tylenol", "morphine", "oxycodone", "hydrocodone", "tramadol",
                "gabapentin", "pregabalin", "sertraline", "citalopram", "escitalopram",
                "fluoxetine", "prozac", "zoloft", "lexapro", "trazodone",
                "alprazolam", "xanax", "lorazepam", "ativan", "clonazepam",
                "klonopin", "levothyroxine", "synthroid", "metoprolol", "carvedilol",
                "furosemide", "lasix", "spironolactone", "digoxin", "amiodarone",
                "diltiazem", "verapamil", "nitroglycerin", "isosorbide", "sildenafil",
                "viagra", "tadalafil", "cialis", "finasteride", "tamsulosin",
                "doxazosin", "terazosin", "ciprofloxacin", "levofloxacin",
                "amoxicillin", "azithromycin", "clarithromycin", "doxycycline",
                "cephalexin", "trimethoprim", "sulfamethoxazole", "bactrim"
            },
            
            EntityType.PROCEDURE: {
                # Common procedures
                "appendectomy", "cholecystectomy", "colonoscopy", "endoscopy",
                "bronchoscopy", "cystoscopy", "arthroscopy", "laparoscopy",
                "thoracotomy", "craniotomy", "mastectomy", "hysterectomy",
                "prostatectomy", "nephrectomy", "splenectomy", "thyroidectomy",
                "tonsillectomy", "adenoidectomy", "cataract surgery",
                "coronary angioplasty", "cardiac catheterization", "pacemaker",
                "defibrillator", "stent", "bypass surgery", "cabg",
                "valve replacement", "transplant", "dialysis", "hemodialysis",
                "peritoneal dialysis", "chemotherapy", "radiation therapy",
                "surgery", "operation", "biopsy", "incision", "excision",
                "resection", "repair", "reconstruction", "implantation",
                "insertion", "removal", "drainage", "suture", "stapling"
            },
            
            EntityType.ANATOMY: {
                # Anatomical structures
                "heart", "lung", "lungs", "liver", "kidney", "kidneys", "brain",
                "head", "neck", "chest", "abdomen", "pelvis", "back", "spine",
                "arm", "arms", "leg", "legs", "hand", "hands", "foot", "feet",
                "eye", "eyes", "ear", "ears", "nose", "mouth", "throat",
                "stomach", "intestine", "colon", "rectum", "bladder", "prostate",
                "uterus", "ovary", "ovaries", "breast", "breasts", "skin",
                "muscle", "muscles", "bone", "bones", "joint", "joints",
                "artery", "arteries", "vein", "veins", "blood vessel",
                "coronary artery", "aorta", "pulmonary artery", "carotid artery",
                "femoral artery", "renal artery", "hepatic artery", "splenic artery"
            },
            
            EntityType.SIGN_SYMPTOM: {
                # Signs and symptoms
                "fever", "pain", "nausea", "vomiting", "diarrhea", "constipation",
                "fatigue", "weakness", "dizziness", "headache", "cough",
                "shortness of breath", "dyspnea", "chest pain", "abdominal pain",
                "back pain", "joint pain", "muscle pain", "sore throat",
                "runny nose", "congestion", "sneezing", "rash", "itching",
                "swelling", "edema", "bruising", "bleeding", "weight loss",
                "weight gain", "loss of appetite", "increased appetite",
                "night sweats", "chills", "hot flashes", "palpitations",
                "irregular heartbeat", "high blood pressure", "low blood pressure",
                "rapid heart rate", "slow heart rate", "difficulty breathing",
                "wheezing", "hoarseness", "difficulty swallowing", "heartburn",
                "acid reflux", "bloating", "gas", "cramping", "urgency",
                "frequency", "burning", "numbness", "tingling", "stiffness"
            }
        }
    
    def initialize(self):
        """Initialize the NER annotator."""
        if self.use_model and HAS_SPACY:
            try:
                # Try to load clinical models
                model_options = [
                    self.model_name,
                    "en_core_sci_sm",  # scispaCy small
                    "en_core_sci_md",  # scispaCy medium  
                    "en_ner_bc5cdr_md",  # BioBERT for diseases and chemicals
                    "en_core_web_sm"   # Fallback to general model
                ]
                
                for model in model_options:
                    try:
                        self.nlp = spacy.load(model)
                        print(f"Loaded NER model: {model}")
                        break
                    except OSError:
                        continue
                
                if self.nlp is None:
                    print("No spaCy models found, using rule-based NER only")
                    
            except Exception as e:
                print(f"Error loading NER model: {e}")
                self.nlp = None
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Perform clinical NER on the document."""
        entities = []
        
        # Model-based NER
        if self.use_model and self.nlp is not None:
            entities.extend(self._model_based_ner(document))
        
        # Rule-based NER
        if self.use_rules:
            entities.extend(self._rule_based_ner(document))
        
        # Remove duplicates and overlaps
        entities = self._resolve_overlaps(entities)
        
        return entities
    
    def _model_based_ner(self, document: Document) -> List[NamedEntityAnnotation]:
        """Use spaCy model for NER."""
        doc = self.nlp(document.text)
        entities = []
        
        for ent in doc.ents:
            # Map spaCy entity types to our types
            entity_type = self._map_spacy_label(ent.label_)
            
            if entity_type:
                span = Span(start=ent.start_char, end=ent.end_char)
                entity = NamedEntityAnnotation(
                    span=span,
                    text=ent.text,
                    annotation_type=AnnotationType.NAMED_ENTITY,
                    entity_type=entity_type,
                    confidence=0.9,
                    metadata={
                        "model_label": ent.label_,
                        "method": "model"
                    }
                )
                entities.append(entity)
        
        return entities
    
    def _rule_based_ner(self, document: Document) -> List[NamedEntityAnnotation]:
        """Use rule-based approach for NER."""
        text = document.text.lower()
        entities = []
        
        for entity_type, terms in self.entity_dictionaries.items():
            for term in terms:
                # Find all occurrences of the term
                for match in re.finditer(re.escape(term.lower()), text):
                    start, end = match.span()
                    
                    # Verify word boundaries
                    if self._is_valid_match(document.text, start, end, term):
                        span = Span(start=start, end=end)
                        entity = NamedEntityAnnotation(
                            span=span,
                            text=document.text[start:end],
                            annotation_type=AnnotationType.NAMED_ENTITY,
                            entity_type=entity_type,
                            confidence=0.85,
                            metadata={
                                "matched_term": term,
                                "method": "rule"
                            }
                        )
                        entities.append(entity)
        
        return entities
    
    def _map_spacy_label(self, spacy_label: str) -> Optional[EntityType]:
        """Map spaCy entity labels to our entity types."""
        label_mapping = {
            # Standard spaCy labels
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            
            # scispaCy labels
            "DISEASE": EntityType.DISORDER,
            "CHEMICAL": EntityType.MEDICATION,
            
            # BioBERT labels
            "Disease": EntityType.DISORDER,
            "Chemical": EntityType.MEDICATION,
            
            # Custom mappings
            "DISORDER": EntityType.DISORDER,
            "MEDICATION": EntityType.MEDICATION,
            "PROCEDURE": EntityType.PROCEDURE,
            "ANATOMY": EntityType.ANATOMY,
        }
        
        return label_mapping.get(spacy_label)
    
    def _is_valid_match(self, text: str, start: int, end: int, term: str) -> bool:
        """Check if a match is valid (proper word boundaries)."""
        # Check character before
        if start > 0 and text[start - 1].isalnum():
            return False
        
        # Check character after
        if end < len(text) and text[end].isalnum():
            return False
        
        return True
    
    def _resolve_overlaps(self, entities: List[NamedEntityAnnotation]) -> List[NamedEntityAnnotation]:
        """Remove overlapping entities, keeping the highest confidence ones."""
        if not entities:
            return entities
        
        # Sort by start position, then by confidence (descending)
        entities.sort(key=lambda x: (x.start, -x.confidence))
        
        non_overlapping = []
        
        for entity in entities:
            # Check if this entity overlaps with any already selected
            overlaps = False
            for selected in non_overlapping:
                if entity.span.overlaps(selected.span):
                    overlaps = True
                    break
            
            if not overlaps:
                non_overlapping.append(entity)
        
        return non_overlapping


class SimpleClinicalNER(Annotator):
    """Simplified clinical NER for basic use cases."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.medication_patterns = [
            r'\b\w+(?:cillin|mycin|floxacin|prazole|statin|sartan|pril|olol)\b',
            r'\b(?:mg|mcg|ml|cc|units?)\b',
            r'\b\d+\s*(?:mg|mcg|ml|cc|units?)\b'
        ]
        
        self.vital_patterns = [
            r'\b(?:bp|blood pressure)\s*:?\s*\d+/\d+',
            r'\b(?:hr|heart rate)\s*:?\s*\d+',
            r'\b(?:temp|temperature)\s*:?\s*\d+\.?\d*',
            r'\b(?:rr|respiratory rate)\s*:?\s*\d+',
            r'\b(?:o2|oxygen)\s*sat\w*\s*:?\s*\d+%?'
        ]
    
    def initialize(self):
        """Initialize simple NER."""
        pass
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Simple pattern-based NER."""
        entities = []
        text = document.text
        
        # Find medication-like patterns
        for pattern in self.medication_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                span = Span(start=match.start(), end=match.end())
                entity = NamedEntityAnnotation(
                    span=span,
                    text=match.group(),
                    annotation_type=AnnotationType.NAMED_ENTITY,
                    entity_type=EntityType.MEDICATION,
                    confidence=0.7,
                    metadata={"pattern": pattern}
                )
                entities.append(entity)
        
        # Find vital sign patterns
        for pattern in self.vital_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                span = Span(start=match.start(), end=match.end())
                entity = NamedEntityAnnotation(
                    span=span,
                    text=match.group(),
                    annotation_type=AnnotationType.NAMED_ENTITY,
                    entity_type=EntityType.LAB_VALUE,
                    confidence=0.8,
                    metadata={"pattern": pattern, "type": "vital_sign"}
                )
                entities.append(entity)
        
        return entities
