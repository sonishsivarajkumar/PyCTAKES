# PyTAKES

![PyTAKES Logo](https://img.shields.io/badge/PyTAKES-Clinical%20NLP-teal?style=for-the-badge)

**Python-native clinical NLP framework that mirrors and extends Apache cTAKES**

[![PyPI version](https://badge.fury.io/py/pytakes.svg)](https://badge.fury.io/py/pytakes)
[![Python versions](https://img.shields.io/pypi/pyversions/pytakes.svg)](https://pypi.org/project/pytakes/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/sonish777/pytakes/workflows/CI/badge.svg)](https://github.com/sonish777/pytakes/actions)
[![Documentation Status](https://readthedocs.org/projects/pytakes/badge/?version=latest)](https://pytakes.readthedocs.io/en/latest/?badge=latest)

---

## 🏥 What is PyTAKES?

PyTAKES is a comprehensive, modern clinical Natural Language Processing framework built entirely in Python. It provides end-to-end clinical text processing capabilities that match and extend Apache cTAKES functionality while being easier to install, use, and extend.

## ✨ Key Features

### 🔬 Complete Clinical NLP Pipeline
- **Sentence Segmentation**: Clinical-aware boundary detection with abbreviation handling
- **Tokenization**: Advanced tokenization with POS tagging and lemmatization
- **Section Detection**: Automatic identification of clinical sections (History, Medications, Assessment, etc.)
- **Named Entity Recognition**: Medical entity extraction (disorders, medications, procedures, anatomy)
- **Negation & Assertion**: pyConText-style negation and assertion detection
- **Concept Mapping**: UMLS integration with CUI normalization

### ⚡ Multiple Pipeline Configurations
- **Default Pipeline**: Full clinical NLP with all features
- **Fast Pipeline**: Speed-optimized with rule-based components
- **Basic Pipeline**: Minimal set for simple use cases
- **Custom Pipeline**: Build your own with configurable annotators

### 🚀 Production Ready
- Pure Python implementation (no Java dependencies)
- Command-line interface and comprehensive Python API
- Extensive error handling and fallback mechanisms
- Comprehensive testing and documentation

## 📦 Quick Start

### Installation

```bash
pip install pytakes
```

### Basic Usage

```python
import pytakes

# Create a clinical NLP pipeline
pipeline = pytakes.create_default_pipeline()

# Process clinical text
clinical_text = """
Patient is a 65-year-old male with diabetes and hypertension.
He presents with chest pain but denies shortness of breath.
Current medications include metformin and lisinopril.
"""

result = pipeline.process_text(clinical_text)

# Access different types of annotations
entities = result.document.get_annotations("NAMED_ENTITY")
for entity in entities:
    print(f"{entity.text} -> {entity.entity_type.value}")
```

**Output:**
```
diabetes -> disorder
hypertension -> disorder  
chest pain -> disorder
shortness of breath -> sign_symptom
metformin -> medication
lisinopril -> medication
```

### Command Line Usage

```bash
# Annotate a clinical note
pytakes annotate clinical_note.txt --output annotations.json

# Use different pipeline types
pytakes annotate clinical_note.txt --pipeline fast --format text
```

## 🏗️ Architecture

PyTAKES follows a modular, pipeline-based architecture:

```mermaid
graph LR
    A[Clinical Text] --> B[Sentence Segmentation]
    B --> C[Tokenization]
    C --> D[Section Detection]
    D --> E[Named Entity Recognition]
    E --> F[Assertion Detection]
    F --> G[Concept Mapping]
    G --> H[Structured Output]
```

## 📊 Performance

| Pipeline Type | Speed | Features | Use Case |
|---------------|-------|----------|----------|
| **Basic** | ⚡⚡⚡ | Essential NLP | Development, Testing |
| **Fast** | ⚡⚡ | Rule-based | High-throughput Processing |
| **Default** | ⚡ | Complete Clinical NLP | Production, Research |

## 🌟 Use Cases

### Clinical Research
- **Electronic Health Record (EHR) Analysis**: Extract structured data from clinical notes
- **Phenotyping**: Identify patient cohorts based on clinical criteria
- **Clinical Trial Recruitment**: Automated patient screening

### Healthcare Analytics
- **Quality Metrics**: Extract quality indicators from clinical documentation
- **Population Health**: Analyze health trends across patient populations
- **Clinical Decision Support**: Real-time analysis of clinical text

### NLP Research
- **Baseline Framework**: Comprehensive clinical NLP baseline
- **Custom Development**: Extensible platform for clinical NLP research
- **Benchmark Comparisons**: Standardized evaluation framework

## 📚 Documentation

- **[Installation Guide](installation.md)** - Detailed setup instructions
- **[Quick Start Tutorial](quickstart.md)** - Get up and running in minutes
- **[User Guide](user-guide/pipeline.md)** - Comprehensive usage documentation
- **[API Reference](api/pipeline.md)** - Complete API documentation
- **[Examples](examples.md)** - Real-world usage examples

## 🤝 Community & Support

- 📂 **GitHub**: [https://github.com/sonish777/pytakes](https://github.com/sonish777/pytakes)
- 📖 **Documentation**: [https://sonish777.github.io/pytakes](https://sonish777.github.io/pytakes)
- 🐛 **Issues**: [GitHub Issues](https://github.com/sonish777/pytakes/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sonish777/pytakes/discussions)

## 🛣️ Roadmap

- **v1.0** ✅ Core clinical NLP pipeline
- **v1.1** 🔄 Relation extraction, Docker support
- **v2.0** 📋 LLM integration, advanced features
- **Future** 🔮 Real-time processing, EHR integration

## 📄 License

PyTAKES is released under the **Apache-2.0 License**. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

PyTAKES is inspired by [Apache cTAKES](https://ctakes.apache.org/) and builds upon the excellent work of the clinical NLP community. Special thanks to the developers of spaCy, scispaCy, and other open-source libraries that make this project possible.

---

**Ready to get started?** Check out our [Quick Start Guide](quickstart.md) or explore the [Examples](examples.md)!

PyTAKES is an entirely Python-based clinical NLP framework that mirrors and extends Apache cTAKES' rich functionality, while delivering an easy-to-install, easy-to-use package on PyPI.

### Key Features

- **Full UIMA-style Pipeline**: Sentence segmentation, tokenization, POS tagging, chunking
- **Named Entity Recognition**: Disorders, medications, procedures, anatomy
- **Concept Mapping**: Automatic mapping to UMLS (SNOMED CT, RxNorm, LOINC)
- **Assertion & Negation**: Integrated pyConText-style rule engine
- **Relation Extraction**: Rule-based and transformer-based approaches
- **Agentic LLM Layer**: LangChain-powered intelligent processing
- **Easy Installation**: `pip install pytakes`

### Quick Example

```python
from pytakes import Pipeline

# Initialize pipeline
pipeline = Pipeline()

# Process clinical text
text = "Patient has diabetes and hypertension. No known allergies."
result = pipeline.process_text(text)

# Access annotations
for annotation in result.document.annotations:
    print(f"{annotation.text} -> {annotation.annotation_type}")
```

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
