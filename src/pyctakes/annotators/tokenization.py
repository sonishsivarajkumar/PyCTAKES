"""Clinical tokenization and sentence segmentation annotators."""

import re
from typing import List, Optional

try:
    import spacy
    from spacy.lang.en import English
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False

try:
    import stanza
    HAS_STANZA = True
except ImportError:
    HAS_STANZA = False

from ..types import (
    Document, Annotation, Span, AnnotationType, 
    TokenAnnotation, SentenceAnnotation
)
from .base import Annotator


class ClinicalSentenceSegmenter(Annotator):
    """Clinical-aware sentence segmentation."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.nlp = None
        self.backend = self.get_config("backend", "spacy")  # "spacy" or "stanza"
        
        # Clinical abbreviations that shouldn't trigger sentence breaks
        self.clinical_abbrevs = {
            "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "vs.", "etc.", "Inc.", "Ltd.",
            "mg.", "mcg.", "ml.", "cc.", "cm.", "mm.", "kg.", "lb.", "oz.",
            "b.i.d.", "t.i.d.", "q.i.d.", "p.r.n.", "p.o.", "i.v.", "i.m.",
            "pt.", "pts.", "dx.", "hx.", "tx.", "sx.", "rx.", "fx.", "bx.",
            "c/o", "s/p", "w/o", "w/", "pt", "pts", "dx", "hx", "tx", "sx",
            "No.", "yr.", "yrs.", "mo.", "mos.", "wk.", "wks.", "d.", "hr.", "hrs.",
            "min.", "mins.", "sec.", "secs.", "temp.", "resp.", "b.p.", "h.r.",
            "Pt.", "Pts.", "Dx.", "Hx.", "Tx.", "Sx.", "Rx.", "Fx.", "Bx."
        }
    
    def initialize(self):
        """Initialize the sentence segmenter."""
        if self.backend == "spacy" and HAS_SPACY:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Fallback to basic English model
                self.nlp = English()
                self.nlp.add_pipe("sentencizer")
        elif self.backend == "stanza" and HAS_STANZA:
            self.nlp = stanza.Pipeline('en', processors='tokenize', use_gpu=False)
        else:
            # Fallback to rule-based segmentation
            self.nlp = None
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Segment document into sentences."""
        if self.nlp is None:
            return self._rule_based_segmentation(document)
        
        if self.backend == "spacy":
            return self._spacy_segmentation(document)
        elif self.backend == "stanza":
            return self._stanza_segmentation(document)
        else:
            return self._rule_based_segmentation(document)
    
    def _spacy_segmentation(self, document: Document) -> List[SentenceAnnotation]:
        """Use spaCy for sentence segmentation."""
        doc = self.nlp(document.text)
        sentences = []
        
        for sent in doc.sents:
            span = Span(start=sent.start_char, end=sent.end_char)
            sentence = SentenceAnnotation(
                span=span,
                text=sent.text,
                annotation_type=AnnotationType.SENTENCE,
                confidence=0.95
            )
            sentences.append(sentence)
        
        return sentences
    
    def _stanza_segmentation(self, document: Document) -> List[SentenceAnnotation]:
        """Use Stanza for sentence segmentation."""
        doc = self.nlp(document.text)
        sentences = []
        
        for sent in doc.sentences:
            start = sent.tokens[0].start_char
            end = sent.tokens[-1].end_char
            span = Span(start=start, end=end)
            
            sentence = SentenceAnnotation(
                span=span,
                text=document.text[start:end],
                annotation_type=AnnotationType.SENTENCE,
                confidence=0.95
            )
            sentences.append(sentence)
        
        return sentences
    
    def _rule_based_segmentation(self, document: Document) -> List[SentenceAnnotation]:
        """Fallback rule-based sentence segmentation."""
        text = document.text
        sentences = []
        
        # Simple regex-based sentence splitting with clinical awareness
        pattern = r'([.!?]+)\s+'
        splits = re.split(pattern, text)
        
        current_pos = 0
        current_sentence = ""
        
        for i, segment in enumerate(splits):
            if i % 2 == 0:  # Text segment
                current_sentence += segment
            else:  # Punctuation segment
                current_sentence += segment
                
                # Check if this is a real sentence boundary
                if self._is_sentence_boundary(current_sentence.strip()):
                    sentence_text = current_sentence.strip()
                    if sentence_text:
                        span = Span(start=current_pos, end=current_pos + len(sentence_text))
                        sentence = SentenceAnnotation(
                            span=span,
                            text=sentence_text,
                            annotation_type=AnnotationType.SENTENCE,
                            confidence=0.85
                        )
                        sentences.append(sentence)
                    
                    current_pos += len(current_sentence)
                    current_sentence = ""
        
        # Handle remaining text
        if current_sentence.strip():
            sentence_text = current_sentence.strip()
            span = Span(start=current_pos, end=current_pos + len(sentence_text))
            sentence = SentenceAnnotation(
                span=span,
                text=sentence_text,
                annotation_type=AnnotationType.SENTENCE,
                confidence=0.85
            )
            sentences.append(sentence)
        
        return sentences
    
    def _is_sentence_boundary(self, text: str) -> bool:
        """Check if text represents a real sentence boundary."""
        # Check for common clinical abbreviations
        words = text.split()
        if len(words) > 0:
            last_word = words[-1]
            if last_word in self.clinical_abbrevs:
                return False
        
        # Check for other patterns that shouldn't be sentence boundaries
        if re.search(r'\d+\.\s*\d+', text):  # Numbers like "1.5"
            return False
        
        return True


class ClinicalTokenizer(Annotator):
    """Clinical-aware tokenization with POS tagging."""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.nlp = None
        self.backend = self.get_config("backend", "spacy")
        self.include_pos = self.get_config("include_pos", True)
        self.include_lemma = self.get_config("include_lemma", True)
        
        # Clinical-specific patterns
        self.clinical_patterns = [
            r'\b\d+\.\d+\b',  # Dosages like "2.5"
            r'\b\d+/\d+\b',   # Ratios like "120/80"
            r'\b\d+mg\b',     # Medication dosages
            r'\b\d+mcg\b',    # Medication dosages
            r'\b\d+ml\b',     # Volumes
            r'\b\d+cc\b',     # Volumes
            r'\b\d+%\b',      # Percentages
            r'\b\d+-\d+\b',   # Ranges like "10-20"
        ]
    
    def initialize(self):
        """Initialize the tokenizer."""
        if self.backend == "spacy" and HAS_SPACY:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                try:
                    self.nlp = English()
                    if self.include_pos:
                        self.nlp.add_pipe("tagger")
                except Exception:
                    # If spaCy fails completely, fall back to rule-based
                    self.nlp = None
        elif self.backend == "stanza" and HAS_STANZA:
            try:
                processors = "tokenize"
                if self.include_pos:
                    processors += ",pos"
                if self.include_lemma:
                    processors += ",lemma"
                self.nlp = stanza.Pipeline('en', processors=processors, use_gpu=False)
            except Exception:
                # If Stanza fails, fall back to rule-based
                self.nlp = None
        else:
            self.nlp = None
    
    def annotate(self, document: Document) -> List[Annotation]:
        """Tokenize the document."""
        if self.nlp is None:
            return self._rule_based_tokenization(document)
        
        if self.backend == "spacy":
            return self._spacy_tokenization(document)
        elif self.backend == "stanza":
            return self._stanza_tokenization(document)
        else:
            return self._rule_based_tokenization(document)
    
    def _spacy_tokenization(self, document: Document) -> List[TokenAnnotation]:
        """Use spaCy for tokenization."""
        doc = self.nlp(document.text)
        tokens = []
        
        for token in doc:
            # Skip whitespace tokens
            if token.text.strip():
                span = Span(start=token.idx, end=token.idx + len(token.text))
                
                token_ann = TokenAnnotation(
                    span=span,
                    text=token.text,
                    annotation_type=AnnotationType.TOKEN,
                    confidence=0.95,
                    pos_tag=token.pos_ if self.include_pos else None,
                    lemma=token.lemma_ if self.include_lemma else None,
                    is_stop=token.is_stop
                )
                tokens.append(token_ann)
        
        return tokens
    
    def _stanza_tokenization(self, document: Document) -> List[TokenAnnotation]:
        """Use Stanza for tokenization."""
        doc = self.nlp(document.text)
        tokens = []
        
        for sentence in doc.sentences:
            for token in sentence.tokens:
                word = token.words[0]  # Get first word of token
                
                span = Span(start=token.start_char, end=token.end_char)
                
                token_ann = TokenAnnotation(
                    span=span,
                    text=token.text,
                    annotation_type=AnnotationType.TOKEN,
                    confidence=0.95,
                    pos_tag=word.pos if self.include_pos else None,
                    lemma=word.lemma if self.include_lemma else None,
                    is_stop=False  # Stanza doesn't provide stop word info
                )
                tokens.append(token_ann)
        
        return tokens
    
    def _rule_based_tokenization(self, document: Document) -> List[TokenAnnotation]:
        """Fallback rule-based tokenization."""
        text = document.text
        tokens = []
        
        # Handle clinical patterns first
        clinical_matches = []
        for pattern in self.clinical_patterns:
            for match in re.finditer(pattern, text):
                clinical_matches.append((match.start(), match.end(), match.group()))
        
        # Sort by position
        clinical_matches.sort(key=lambda x: x[0])
        
        # Basic word tokenization
        word_pattern = r'\b\w+\b'
        current_pos = 0
        
        for match in re.finditer(word_pattern, text):
            start, end = match.span()
            token_text = match.group()
            
            # Skip if this is part of a clinical pattern
            is_clinical = False
            for clin_start, clin_end, clin_text in clinical_matches:
                if start >= clin_start and end <= clin_end:
                    is_clinical = True
                    break
            
            if not is_clinical:
                span = Span(start=start, end=end)
                token_ann = TokenAnnotation(
                    span=span,
                    text=token_text,
                    annotation_type=AnnotationType.TOKEN,
                    confidence=0.8
                )
                tokens.append(token_ann)
        
        # Add clinical patterns as tokens
        for clin_start, clin_end, clin_text in clinical_matches:
            span = Span(start=clin_start, end=clin_end)
            token_ann = TokenAnnotation(
                span=span,
                text=clin_text,
                annotation_type=AnnotationType.TOKEN,
                confidence=0.9,
                metadata={"clinical_pattern": True}
            )
            tokens.append(token_ann)
        
        # Sort tokens by position
        tokens.sort(key=lambda x: x.start)
        
        return tokens
