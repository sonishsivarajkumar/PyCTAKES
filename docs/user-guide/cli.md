# Command Line Interface

PyCTAKES provides a comprehensive command-line interface for processing clinical text without writing code.

## Basic Usage

```bash
# Process a single file
pyctakes process input.txt

# Process with output file
pyctakes process input.txt --output output.json

# Process multiple files
pyctakes process *.txt --output-dir results/

# Use custom configuration
pyctakes process input.txt --config my_config.json
```

## Commands

### process

Process clinical text files through the PyCTAKES pipeline.

```bash
pyctakes process [OPTIONS] INPUT_FILES...
```

**Arguments:**
- `INPUT_FILES`: One or more input text files to process

**Options:**
- `--output, -o TEXT`: Output file path (default: stdout)
- `--output-dir, -d TEXT`: Output directory for multiple files
- `--config, -c TEXT`: Configuration file path
- `--pipeline, -p TEXT`: Pipeline name (default, fast, basic, custom)
- `--format, -f TEXT`: Output format (json, xml, text)
- `--verbose, -v`: Enable verbose logging
- `--quiet, -q`: Suppress all output except results

**Examples:**

```bash
# Basic processing
pyctakes process note.txt

# Save to file
pyctakes process note.txt --output results.json

# Process multiple files
pyctakes process notes/*.txt --output-dir processed/

# Use fast pipeline
pyctakes process note.txt --pipeline fast

# Custom configuration
pyctakes process note.txt --config my_config.json --verbose
```

### configure

Create and manage configuration files.

```bash
pyctakes configure [OPTIONS]
```

**Options:**
- `--create, -c TEXT`: Create new configuration file
- `--template, -t TEXT`: Use template (default, fast, basic, medication)
- `--edit, -e TEXT`: Edit existing configuration
- `--validate, -v TEXT`: Validate configuration file

**Examples:**

```bash
# Create default configuration
pyctakes configure --create config.json

# Create from template
pyctakes configure --create fast_config.json --template fast

# Validate configuration
pyctakes configure --validate my_config.json
```

### info

Display information about PyCTAKES installation and capabilities.

```bash
pyctakes info [OPTIONS]
```

**Options:**
- `--annotators`: List available annotators
- `--pipelines`: List available pipeline templates
- `--version`: Show version information
- `--dependencies`: Show dependency status

**Examples:**

```bash
# General information
pyctakes info

# List annotators
pyctakes info --annotators

# Check dependencies
pyctakes info --dependencies
```

### demo

Run interactive demonstrations and examples.

```bash
pyctakes demo [OPTIONS]
```

**Options:**
- `--example, -e TEXT`: Run specific example (basic, comprehensive, custom)
- `--interactive, -i`: Interactive mode
- `--sample-text, -s`: Use built-in sample text

**Examples:**

```bash
# Interactive demo
pyctakes demo --interactive

# Run basic example
pyctakes demo --example basic

# Use sample text
pyctakes demo --sample-text
```

## Output Formats

### JSON Format (default)

```json
{
  "text": "Patient has diabetes and hypertension.",
  "sentences": [
    {
      "start": 0,
      "end": 37,
      "text": "Patient has diabetes and hypertension."
    }
  ],
  "tokens": [
    {"start": 0, "end": 7, "text": "Patient"},
    {"start": 8, "end": 11, "text": "has"},
    {"start": 12, "end": 20, "text": "diabetes"}
  ],
  "entities": [
    {
      "start": 12,
      "end": 20,
      "text": "diabetes",
      "label": "CONDITION",
      "assertion": {
        "polarity": "POSITIVE",
        "uncertainty": "CERTAIN"
      }
    }
  ],
  "sections": [
    {
      "start": 0,
      "end": 37,
      "section_type": "ASSESSMENT_AND_PLAN"
    }
  ]
}
```

### XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<document>
  <text>Patient has diabetes and hypertension.</text>
  <annotations>
    <sentence start="0" end="37">Patient has diabetes and hypertension.</sentence>
    <entity start="12" end="20" label="CONDITION" polarity="POSITIVE">diabetes</entity>
    <entity start="25" end="37" label="CONDITION" polarity="POSITIVE">hypertension</entity>
  </annotations>
</document>
```

### Text Format

```
TEXT: Patient has diabetes and hypertension.

ENTITIES:
- diabetes (CONDITION) [12-20] POSITIVE/CERTAIN
- hypertension (CONDITION) [25-37] POSITIVE/CERTAIN

SECTIONS:
- ASSESSMENT_AND_PLAN [0-37]
```

## Pipeline Templates

### default

Complete clinical NLP pipeline with all annotators:
- Tokenization (spaCy)
- Section detection
- Named entity recognition (rule-based)
- Assertion detection
- UMLS concept mapping

```bash
pyctakes process note.txt --pipeline default
```

### fast

Optimized for speed with basic functionality:
- Tokenization (rule-based)
- Named entity recognition (rule-based)
- Basic assertion detection

```bash
pyctakes process note.txt --pipeline fast
```

### basic

Minimal pipeline for simple entity extraction:
- Tokenization (rule-based)
- Named entity recognition (rule-based)

```bash
pyctakes process note.txt --pipeline basic
```

### custom

User-defined pipeline from configuration file:

```bash
pyctakes process note.txt --pipeline custom --config my_pipeline.json
```

## Configuration Examples

### Create Basic Configuration

```bash
pyctakes configure --create basic_config.json --template basic
```

Creates:
```json
{
  "tokenization": {
    "backend": "rule_based"
  },
  "ner": {
    "approach": "rule_based",
    "entity_types": ["MEDICATION", "CONDITION", "SYMPTOM"]
  }
}
```

### Medication-Focused Configuration

```bash
pyctakes configure --create med_config.json --template medication
```

Creates configuration optimized for medication extraction.

## Batch Processing

### Process Directory

```bash
# Process all .txt files in a directory
pyctakes process input_dir/*.txt --output-dir results/

# Process with specific pattern
pyctakes process "notes_*.txt" --output-dir processed/
```

### Parallel Processing

```bash
# Process files in parallel (if supported)
pyctakes process *.txt --output-dir results/ --parallel --workers 4
```

## Advanced Usage

### Custom Output

```bash
# Only output entities
pyctakes process note.txt --format json --filter entities

# Include confidence scores
pyctakes process note.txt --include-confidence

# Minimal output
pyctakes process note.txt --minimal
```

### Logging and Debugging

```bash
# Verbose logging
pyctakes process note.txt --verbose

# Debug mode
pyctakes process note.txt --debug

# Log to file
pyctakes process note.txt --log-file processing.log
```

### Performance Monitoring

```bash
# Show timing information
pyctakes process note.txt --timing

# Profile performance
pyctakes process note.txt --profile
```

## Integration Examples

### Shell Scripting

```bash
#!/bin/bash
# Process all patient notes
for file in patient_notes/*.txt; do
    echo "Processing $file..."
    pyctakes process "$file" --output "results/$(basename "$file" .txt).json"
done
```

### Pipeline Integration

```bash
# Use in pipeline
cat input.txt | pyctakes process - --format json | jq '.entities[].text'

# With other tools
pyctakes process notes/*.txt --output-dir results/ && \
    python analyze_results.py results/
```

## Error Handling

```bash
# Continue on errors
pyctakes process *.txt --continue-on-error

# Skip invalid files
pyctakes process *.txt --skip-invalid

# Error reporting
pyctakes process *.txt --error-report errors.log
```

## Help and Documentation

```bash
# General help
pyctakes --help

# Command-specific help
pyctakes process --help
pyctakes configure --help

# Show examples
pyctakes examples

# Version information
pyctakes --version
```
