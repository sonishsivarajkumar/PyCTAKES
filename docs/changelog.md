# Changelog

All notable changes to PyTAKES will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive API documentation with mkdocstrings
- Advanced topics documentation (custom annotators, performance tuning, UMLS integration)
- Development and contributing guidelines
- GitHub Actions workflow for documentation deployment

### Changed
- Enhanced mkdocs configuration with material theme
- Improved navigation structure for documentation

## [1.0.0] - 2025-01-15

### Added
- Core pipeline architecture with configurable annotator chains
- Clinical text processing annotators:
  - `ClinicalSentenceSegmenter` - Clinical-aware sentence segmentation
  - `ClinicalTokenizer` - Advanced tokenization with POS tagging
  - `ClinicalSectionAnnotator` - Clinical document section detection
- Named entity recognition:
  - `ClinicalNERAnnotator` - Hybrid rule-based and model-based NER
  - `SimpleClinicalNER` - Fast pattern-based entity recognition
- Assertion and negation detection:
  - `NegationAssertionAnnotator` - pyConText-style context detection
- UMLS concept mapping:
  - `UMLSConceptMapper` - Framework for UMLS integration
  - `SimpleDictionaryMapper` - Fast dictionary-based mapping
- Three pre-configured pipeline types:
  - Default pipeline - Full clinical NLP features
  - Fast pipeline - Speed-optimized with rule-based components
  - Basic pipeline - Minimal entity extraction
- Command-line interface with multiple output formats
- Comprehensive type system for clinical text annotations
- Configuration-driven annotator behavior
- Extensive test suite with unit and integration tests
- Performance benchmarking and metrics
- Documentation with installation, quickstart, and user guides
- Example configurations and sample clinical notes

### Technical Features
- Multiple backend support (spaCy, Stanza, rule-based)
- Clinical abbreviation awareness in tokenization
- Comprehensive clinical entity dictionaries (100+ terms per category)
- Bidirectional context analysis for assertion detection
- Configurable pipeline composition and annotator parameters
- Error handling and recovery throughout processing pipeline
- JSON serialization for all annotation types
- Memory-efficient processing with streaming capabilities

### Documentation
- Complete installation and setup instructions
- Quickstart guide with basic usage examples
- Comprehensive user guide covering all features
- API reference documentation
- Configuration examples and best practices
- Performance optimization guidelines

### Performance
- Basic Pipeline: 39 annotations in 0.010s
- Fast Pipeline: 36 annotations in 0.001s
- Full clinical note processing: 81 annotations in 0.504s

## [0.1.0] - 2025-01-01

### Added
- Initial project structure and setup
- Basic pipeline framework
- Core type definitions
- Development environment configuration
- CI/CD pipeline setup

---

## Release Notes

### Version 1.0.0 - "Foundation Release"

PyTAKES v1.0.0 represents the first stable release of our Python-native clinical NLP framework. This release delivers comprehensive feature parity with Apache cTAKES while providing modern Python APIs and superior usability.

**Key Highlights:**
- 🏥 **Clinical-First Design**: Built specifically for clinical text processing with medical abbreviation awareness, section detection, and assertion analysis
- 🚀 **Multiple Pipeline Types**: Choose from default, fast, or basic pipelines based on your accuracy/speed requirements  
- 🔧 **Flexible Architecture**: Modular annotator system allows custom pipeline composition and easy extensibility
- 📊 **Production Ready**: Comprehensive testing, error handling, and performance optimization for real-world deployment
- 📖 **Complete Documentation**: Full user guides, API documentation, and practical examples

**Migration from cTAKES:**
PyTAKES provides a drop-in replacement for Apache cTAKES with simpler deployment (no Java required) and modern NLP backends. Existing cTAKES users can migrate their pipelines using our configuration system.

**Next Steps:**
- Enhanced UMLS integration with full QuickUMLS support
- Relation extraction for temporal and dosage relationships
- REST API service wrapper
- Performance optimizations and Docker containers

**Community:**
PyTAKES is open source and welcoming contributions. Join us in advancing clinical NLP with modern Python tools!

---

## Version Scheme

PyTAKES follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions  
- **PATCH** version for backwards-compatible bug fixes

### Pre-release Identifiers

- **alpha** (a): Early development versions
- **beta** (b): Feature-complete but potentially unstable
- **rc**: Release candidates, stable and ready for release

Example: `1.1.0a1` (first alpha of version 1.1.0)

## Release Schedule

- **Major releases**: Annually or for significant architectural changes
- **Minor releases**: Quarterly for new features
- **Patch releases**: As needed for critical bug fixes

## Deprecation Policy

- Features marked as deprecated will be removed in the next major version
- Deprecation warnings will be issued for at least one minor version before removal
- Migration guides will be provided for deprecated features

## Breaking Changes

All breaking changes will be clearly documented with:
- Description of the change
- Reason for the change  
- Migration instructions
- Timeline for old behavior removal

## Support

- **Current major version**: Full support with bug fixes and new features
- **Previous major version**: Security updates and critical bug fixes for 12 months
- **Older versions**: Community support only
