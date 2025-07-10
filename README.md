# pyCTAKES 🏥
## Open Source Python-native Clinical NLP Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/sonishsivarajkumar/PyCTAKES)](https://github.com/sonishsivarajkumar/PyCTAKES/issues)
[![GitHub stars](https://img.shields.io/github/stars/sonishsivarajkumar/PyCTAKES)](https://github.com/sonishsivarajkumar/PyCTAKES/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sonishsivarajkumar/PyCTAKES)](https://github.com/sonishsivarajkumar/PyCTAKES/network)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/sonishsivarajkumar/PyCTAKES/blob/main/CONTRIBUTING.md)

> **🚀 A modern, open source clinical NLP framework** that mirrors and extends Apache cTAKES functionality in pure Python. Drop-in replacement with superior usability, extensibility, and performance.

**pyCTAKES** transforms clinical text processing by providing a **100% open source**, Python-native alternative to Apache cTAKES. Built by the community, for the community - no vendor lock-in, no licensing fees, just powerful clinical NLP tools that anyone can use, modify, and contribute to.

---

## 🌟 Why Choose pyCTAKES?

<table>
<tr>
<td>

### 🔓 **Fully Open Source**
- **MIT License** - Free for commercial & research use
- **Transparent development** - All code, issues, and discussions public
- **Community-driven** - Shaped by real user needs
- **No vendor lock-in** - Own your clinical NLP pipeline

</td>
<td>

### ⚡ **Modern & Fast**
- **Pure Python** - No Java dependencies
- **pip installable** - Get started in seconds
- **Multiple backends** - spaCy, Stanza, rule-based
- **Production ready** - Optimized for real-world use

</td>
</tr>
<tr>
<td>

### 🏥 **Clinical-First Design**
- **Medical expertise built-in** - Clinical abbreviations, sections, terminology
- **cTAKES compatibility** - Drop-in replacement for existing workflows
- **Comprehensive NLP** - Tokenization → UMLS mapping
- **Assertion detection** - Negation, uncertainty, temporal context

</td>
<td>

### 🔧 **Developer Friendly**
- **Clean Python APIs** - Intuitive and well-documented
- **Modular architecture** - Use only what you need
- **Extensible framework** - Easy to add custom annotators
- **Rich ecosystem** - Integrates with pandas, spaCy, transformers

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Installation
```bash
pip install pyctakes
```

### 30-Second Demo
```python
import pyctakes

# Create pipeline
pipeline = pyctakes.create_default_pipeline()

# Process clinical text
clinical_note = """
Patient is a 65-year-old male with diabetes and hypertension.
He denies chest pain but reports shortness of breath.
Current medications: metformin 500mg BID, lisinopril 10mg daily.
"""

result = pipeline.process_text(clinical_note)

# Explore results
print(f"Found {len(result.entities)} clinical entities:")
for entity in result.entities[:3]:
    assertion = entity.assertion
    print(f"  • {entity.text} ({entity.label})")
    print(f"    → {assertion.polarity}, {assertion.uncertainty}")
```

**Output:**
```
Found 8 clinical entities:
  • diabetes (CONDITION)
    → POSITIVE, CERTAIN
  • hypertension (CONDITION)  
    → POSITIVE, CERTAIN
  • chest pain (SYMPTOM)
    → NEGATIVE, CERTAIN
```

---

## 📊 Performance & Features

### ⚡ Blazing Fast Performance
- **Basic Pipeline**: 39 annotations in 0.010s
- **Fast Pipeline**: 36 annotations in 0.001s  
- **Full Clinical Note**: 81 annotations in 0.504s

### 🎯 Comprehensive Clinical NLP

| Feature | Description | Status |
|---------|-------------|--------|
| **Sentence Segmentation** | Clinical-aware sentence boundary detection | ✅ |
| **Tokenization** | Advanced tokenization with POS tagging | ✅ |
| **Section Detection** | Chief Complaint, History, Medications, Assessment, etc. | ✅ |
| **Named Entity Recognition** | Medications, conditions, procedures, anatomy | ✅ |
| **Assertion Detection** | Negation, uncertainty, temporal, experiencer | ✅ |
| **UMLS Concept Mapping** | CUI normalization and semantic types | ✅ |
| **Relation Extraction** | Temporal and dosage relationships | 🔄 v1.1 |
| **REST API Service** | FastAPI deployment wrapper | 🔄 v1.1 |

### 🔧 Three Pipeline Types
```python
# Full-featured (highest accuracy)
pipeline = pyctakes.create_default_pipeline()

# Speed-optimized (fastest processing)  
pipeline = pyctakes.create_fast_pipeline()

# Minimal (basic entity extraction)
pipeline = pyctakes.create_basic_pipeline()
```

---

## 💻 Command Line Interface

```bash
# Process single file
pyctakes process note.txt --output results.json

# Batch processing
pyctakes process notes/*.txt --output-dir results/

# Different pipelines and formats
pyctakes process note.txt --pipeline fast --format xml
pyctakes process note.txt --config custom_config.json
```

---

## 🤝 Open Source Community

### 👥 **Lead Contributors**
- **[Sonish Sivarajkumar](https://github.com/sonishsivarajkumar)** - *Lead Maintainer & Creator*
  - Clinical NLP researcher and software engineer
  - Apache cTAKES community member
  - Python & healthcare technology enthusiast

### 🌍 **Join Our Community**
We're building the future of clinical NLP together! Whether you're a:

- **👩‍⚕️ Clinician** - Help us understand real-world clinical text challenges
- **👨‍💻 Developer** - Contribute code, fix bugs, or add new features  
- **🔬 Researcher** - Share use cases, benchmarks, and domain expertise
- **📚 Technical Writer** - Improve documentation and tutorials
- **🎨 Designer** - Enhance user experience and visualization

**Everyone is welcome!** Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

### 📈 **Community Stats**
- **Contributors**: Growing community of clinical NLP enthusiasts
- **Issues**: Active issue tracking and feature requests
- **Discussions**: Technical discussions and use case sharing
- **Releases**: Regular updates with new features and improvements

### 🎯 **Ways to Contribute**

<table>
<tr>
<td>

**🐛 Report Issues**
- Bug reports
- Feature requests  
- Documentation issues
- Performance problems

</td>
<td>

**💡 Share Ideas**
- New annotators
- Pipeline improvements
- Integration suggestions
- Use case examples

</td>
<td>

**🔧 Code Contributions**
- Bug fixes
- New features
- Performance optimizations
- Test improvements

</td>
<td>

**📖 Documentation**
- API documentation
- Tutorials & guides
- Example notebooks
- Translation support

</td>
</tr>
</table>

---

## 📚 Documentation & Resources

- **📖 [Full Documentation](https://sonishsivarajkumar.github.io/PyCTAKES)** - Complete guides and API reference
- **🚀 [Quick Start Guide](https://sonishsivarajkumar.github.io/PyCTAKES/quickstart/)** - Get up and running in minutes
- **💡 [Examples](examples/)** - Real-world usage examples and configurations
- **🔧 [API Reference](https://sonishsivarajkumar.github.io/PyCTAKES/api/)** - Detailed API documentation
- **⚡ [Performance Guide](https://sonishsivarajkumar.github.io/PyCTAKES/advanced/performance/)** - Optimization tips and benchmarks
- **🤝 [Contributing](CONTRIBUTING.md)** - How to contribute to the project

---

## 🗺️ Roadmap

### 🎯 **v1.0** (Current) - Foundation
- ✅ Core pipeline architecture
- ✅ Clinical text processing (tokenization, NER, assertion)
- ✅ UMLS concept mapping framework
- ✅ CLI and Python APIs
- ✅ Comprehensive documentation

### ⚡ **v1.1** (Next) - Enhancement  
- 🔄 Enhanced UMLS integration (QuickUMLS)
- 🔄 Relation extraction (temporal, dosage)
- 🔄 REST API service wrapper
- 🔄 Docker containers & deployment guides
- 🔄 Performance optimizations

### 🚀 **v2.0** (Future) - Intelligence
- 🔮 LLM integration for disambiguation
- 🔮 Active learning capabilities  
- 🔮 Advanced relation extraction
- 🔮 Real-time processing pipelines
- 🔮 Federated learning support

---

## 🏆 Why Open Source Matters in Healthcare

Healthcare technology should be:

- **🔍 Transparent** - Auditable algorithms for patient safety
- **🤝 Collaborative** - Shared knowledge accelerates progress  
- **♿ Accessible** - No barriers to life-saving technology
- **🔧 Customizable** - Adaptable to diverse clinical environments
- **📈 Sustainable** - Community-driven long-term maintenance

PyCTAKES embodies these principles by providing enterprise-grade clinical NLP capabilities as a **truly open source project**. No hidden costs, no vendor dependencies, just powerful tools for advancing healthcare through technology.

---

## 📄 License & Citation

### 📜 **License**
PyCTAKES is released under the **MIT License** - see [LICENSE](LICENSE) for details.

```
Copyright (c) 2025 Sonish Sivarajkumar and Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
[Full license text in LICENSE file]
```

### 📝 **Citation**
If you use PyCTAKES in your research, please cite:

```bibtex
@software{pyctakes2025,
  title={PyCTAKES: Open Source Python-native Clinical NLP Framework},
  author={Sivarajkumar, Sonish and Contributors},
  year={2025},
  url={https://github.com/sonishsivarajkumar/PyCTAKES},
  version={1.0.0}
}
```

---

## 🙏 Acknowledgments

PyCTAKES builds upon the excellent work of:

- **Apache cTAKES** - Pioneering clinical NLP framework
- **spaCy & Stanza** - Modern NLP processing libraries  
- **Clinical NLP Community** - Researchers and practitioners advancing the field
- **Open Source Contributors** - Everyone who helps make this project better

---

## 🚀 Get Started Today!

```bash
# Install PyCTAKES
pip install pyctakes

# Clone the repository
git clone https://github.com/sonishsivarajkumar/PyCTAKES.git
cd PyCTAKES

# Try the examples
python examples/comprehensive_demo.py
```

**Join us in revolutionizing clinical NLP!** 🎉

**[⭐ Star this repo](https://github.com/sonishsivarajkumar/PyCTAKES)** | **[📚 Read the docs](https://sonishsivarajkumar.github.io/PyCTAKES)** | **[🤝 Contribute](CONTRIBUTING.md)** | **[💬 Discuss](https://github.com/sonishsivarajkumar/PyCTAKES/discussions)**