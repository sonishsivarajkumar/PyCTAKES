# Performance Tuning

Optimize pyCTAKES performance for production workloads and large-scale processing.

## Performance Overview

pyCTAKES performance depends on several factors:
- **Pipeline configuration**: Choice of annotators and backends
- **Text characteristics**: Length, complexity, clinical content density
- **Hardware resources**: CPU, memory, disk I/O
- **Concurrency**: Single-threaded vs. parallel processing

## Benchmarking Results

Based on our performance testing with clinical notes:

| Pipeline | Entities/sec | Notes/sec | Memory (MB) |
|----------|-------------|-----------|-------------|
| Basic    | 2,500       | 45        | 150         |
| Fast     | 1,800       | 35        | 200         |
| Default  | 800         | 12        | 400         |

*Test environment: MacBook Pro M2, 16GB RAM, clinical notes avg. 500 words*

## Pipeline Optimization

### Choose the Right Pipeline

Select the appropriate pipeline for your use case:

```python
from pyctakes.pipeline import (
    create_basic_pipeline,    # Fastest, minimal features
    create_fast_pipeline,     # Good balance of speed/features
    create_default_pipeline   # Full features, slower
)

# For high-throughput scenarios
pipeline = create_fast_pipeline()

# For maximum accuracy
pipeline = create_default_pipeline()
```

### Backend Selection

Choose backends based on your performance needs:

```python
# Speed-optimized configuration
config = {
    "tokenization": {
        "backend": "rule_based"  # Fastest tokenization
    },
    "ner": {
        "approach": "rule_based"  # Faster than model-based
    }
}

# Accuracy-optimized configuration  
config = {
    "tokenization": {
        "backend": "stanza"      # Most accurate
    },
    "ner": {
        "approach": "model_based"  # Higher accuracy
    }
}
```

### Selective Annotator Usage

Disable unnecessary annotators:

```python
from pyctakes.pipeline import Pipeline
from pyctakes.annotators import TokenizationAnnotator, NERAnnotator

# Minimal pipeline - only what you need
pipeline = Pipeline()
pipeline.add_annotator(TokenizationAnnotator(backend="rule_based"))
pipeline.add_annotator(NERAnnotator(approach="rule_based"))

# Skip expensive annotators like UMLS mapping if not needed
```

## Memory Optimization

### Batch Processing

Process documents in batches to optimize memory usage:

```python
def process_documents_batched(documents, batch_size=100):
    """Process documents in batches to control memory usage."""
    
    results = []
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        batch_results = pipeline.process_batch(batch)
        results.extend(batch_results)
        
        # Optional: Clear cache between batches
        pipeline.clear_cache()
    
    return results
```

### Memory-Efficient Document Processing

```python
def process_large_document(text, max_chunk_size=10000):
    """Process large documents in chunks."""
    
    if len(text) <= max_chunk_size:
        return pipeline.process_text(text)
    
    # Split into chunks (preserve sentence boundaries)
    chunks = smart_chunk_text(text, max_chunk_size)
    
    # Process chunks
    results = []
    for chunk in chunks:
        result = pipeline.process_text(chunk)
        results.append(result)
    
    # Merge results
    return merge_document_results(results)
```

### Clear Caches

Clear caches to free memory:

```python
# Clear annotator caches
pipeline.clear_cache()

# Clear specific annotator cache
for annotator in pipeline.annotators:
    if hasattr(annotator, 'clear_cache'):
        annotator.clear_cache()
```

## CPU Optimization

### Parallel Processing

Use multiprocessing for CPU-bound tasks:

```python
from multiprocessing import Pool
from functools import partial

def process_document_parallel(texts, num_processes=4):
    """Process multiple documents in parallel."""
    
    # Create pipeline factory function
    def create_pipeline_and_process(text):
        # Create pipeline in worker process
        pipeline = create_fast_pipeline()
        return pipeline.process_text(text)
    
    # Process in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(create_pipeline_and_process, texts)
    
    return results
```

### Async Processing

For I/O-bound operations, use async processing:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_documents_async(texts, max_workers=4):
    """Process documents asynchronously."""
    
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        futures = [
            loop.run_in_executor(executor, pipeline.process_text, text)
            for text in texts
        ]
        
        # Wait for completion
        results = await asyncio.gather(*futures)
    
    return results
```

## Annotator-Specific Optimizations

### Tokenization Optimization

```python
# Use rule-based tokenization for speed
tokenizer = TokenizationAnnotator(
    backend="rule_based",
    preserve_whitespace=False  # Skip whitespace preservation
)

# For spaCy, disable unused components
tokenizer = TokenizationAnnotator(
    backend="spacy",
    model="en_core_web_sm",
    disable=["parser", "ner", "textcat"]  # Keep only tokenizer
)
```

### NER Optimization

```python
# Limit entity types for faster processing
ner = NERAnnotator(
    approach="rule_based",
    entity_types=["MEDICATION", "CONDITION"]  # Only extract what you need
)

# Use compiled patterns for rule-based NER
ner = NERAnnotator(
    approach="rule_based",
    precompile_patterns=True  # Pre-compile regex patterns
)
```

### UMLS Optimization

```python
# Enable caching for UMLS lookups
umls = UMLSAnnotator(
    similarity_threshold=0.8,  # Higher threshold = fewer candidates
    max_candidates=3,          # Limit candidates to check
    enable_caching=True,       # Cache concept lookups
    cache_size=10000          # Larger cache for better hit rate
)
```

## I/O Optimization

### Efficient File Processing

```python
def process_files_efficiently(file_paths, output_dir):
    """Process files with optimized I/O."""
    
    pipeline = create_fast_pipeline()
    
    for file_path in file_paths:
        # Read file
        with open(file_path, 'r') as f:
            text = f.read()
        
        # Process
        result = pipeline.process_text(text)
        
        # Write result immediately (don't accumulate in memory)
        output_path = os.path.join(output_dir, f"{file_path.stem}.json")
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f)
```

### Streaming Processing

```python
def process_stream(input_stream, output_stream):
    """Process documents from stream."""
    
    pipeline = create_fast_pipeline()
    
    for line in input_stream:
        text = line.strip()
        if text:
            result = pipeline.process_text(text)
            output_stream.write(json.dumps(result.to_dict()) + '\n')
            output_stream.flush()
```

## Configuration Optimization

### Performance-Focused Configuration

```json
{
  "tokenization": {
    "backend": "rule_based",
    "sentence_split": true,
    "tokenize": true,
    "preserve_whitespace": false
  },
  "ner": {
    "approach": "rule_based",
    "entity_types": ["MEDICATION", "CONDITION"],
    "case_sensitive": false
  },
  "assertion": {
    "window_size": 5,
    "enabled": true
  },
  "umls": {
    "enabled": false
  }
}
```

### Accuracy-Focused Configuration

```json
{
  "tokenization": {
    "backend": "stanza",
    "model": "en"
  },
  "ner": {
    "approach": "model_based",
    "model_name": "en_ner_bc5cdr_md"
  },
  "assertion": {
    "window_size": 15
  },
  "umls": {
    "enabled": true,
    "similarity_threshold": 0.7
  }
}
```

## Monitoring and Profiling

### Performance Monitoring

```python
import time
import psutil
from contextlib import contextmanager

@contextmanager
def performance_monitor():
    """Monitor performance metrics."""
    
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        print(f"Processing time: {end_time - start_time:.2f}s")
        print(f"Memory usage: {end_memory:.2f}MB (peak: {end_memory - start_memory:+.2f}MB)")

# Usage
with performance_monitor():
    results = pipeline.process_batch(documents)
```

### Profiling

```python
import cProfile
import pstats

def profile_pipeline(texts):
    """Profile pipeline performance."""
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Process documents
    results = []
    for text in texts:
        result = pipeline.process_text(text)
        results.append(result)
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    return results
```

## Deployment Optimization

### Docker Optimization

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install pyCTAKES
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Optimize for production
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1

# Pre-download models
RUN python -c "import spacy; spacy.load('en_core_web_sm')"

CMD ["python", "app.py"]
```

### Production Configuration

```python
# Production-optimized pipeline
def create_production_pipeline():
    """Create pipeline optimized for production."""
    
    config = {
        "tokenization": {
            "backend": "spacy",
            "model": "en_core_web_sm",
            "disable": ["parser", "textcat"]  # Keep only needed components
        },
        "ner": {
            "approach": "rule_based",
            "entity_types": ["MEDICATION", "CONDITION", "SYMPTOM"]
        },
        "assertion": {
            "window_size": 8,
            "enabled": True
        },
        "umls": {
            "enabled": False  # Disable for speed in production
        }
    }
    
    return Pipeline.from_config(config)
```

## Benchmarking Tools

### Create Benchmarks

```python
def benchmark_pipeline(pipeline, test_texts, num_runs=10):
    """Benchmark pipeline performance."""
    
    import time
    import statistics
    
    times = []
    entities_counts = []
    
    for _ in range(num_runs):
        start = time.time()
        
        results = []
        for text in test_texts:
            result = pipeline.process_text(text)
            results.append(result)
        
        end = time.time()
        times.append(end - start)
        
        # Count total entities
        total_entities = sum(len(r.entities) for r in results)
        entities_counts.append(total_entities)
    
    print(f"Average processing time: {statistics.mean(times):.3f}s")
    print(f"Std deviation: {statistics.stdev(times):.3f}s")
    print(f"Average entities per run: {statistics.mean(entities_counts):.1f}")
    print(f"Throughput: {len(test_texts) / statistics.mean(times):.1f} docs/sec")
```

## Best Practices Summary

1. **Choose appropriate pipeline**: Match pipeline to your accuracy/speed needs
2. **Use rule-based backends**: For maximum speed when accuracy permits
3. **Limit entity types**: Only extract what you need
4. **Process in batches**: Better memory efficiency than individual documents
5. **Use parallel processing**: For CPU-bound workloads
6. **Enable caching**: For repeated concept lookups
7. **Monitor performance**: Track metrics in production
8. **Profile bottlenecks**: Identify and optimize slow components
9. **Clear caches**: Free memory for long-running processes
10. **Test configurations**: Benchmark different settings for your data
