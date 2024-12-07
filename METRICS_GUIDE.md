# Stilo Metrics Guide

## Analysis Results Explained

### 1. Metadata
- `filename`: Name of analyzed document
- `file_size`: Size in bytes
- `page_count`: Number of pages
- `timestamp`: Analysis time

### 2. Style Metrics

#### Complexity Metrics
- `complexity.score`: Overall text complexity (0-100)
  - Higher scores indicate more complex writing
  - Components:
    - `vocabulary_contribution`: Impact of vocabulary complexity
    - `syntax_contribution`: Impact of sentence structure
    - `readability_contribution`: Impact of overall readability

- `complexity.level`: Categorical assessment
  - "Low": Easy to understand
  - "Medium": Moderate complexity
  - "High": Complex writing style

#### Consistency Metrics
- `consistency.score`: Writing style consistency (0-1)
  - Higher scores indicate more consistent writing
- `consistency.level`: Categorical assessment

#### Classification
- `classification`: Overall writing style category
  - "Academic": Formal, complex writing
  - "Simple and Structured": Clear, straightforward
  - "Complex and Variable": Advanced but inconsistent
  - "Balanced": Good mix of complexity and clarity

### 3. Writing Patterns

#### Vocabulary Usage
- "Advanced": Rich, diverse vocabulary
- "Moderate": Standard vocabulary level
- "Basic": Simple word choices

#### Sentence Structure
- "Complex": Long, intricate sentences
- "Varied": Mix of sentence types
- "Simple": Straightforward sentences

#### Text Organization
- "Well Structured": Clear organization
- "Moderately Structured": Some organization
- "Loosely Structured": Less organized

### 4. Detailed Features

#### Lexical Features
- `avg_word_length`: Average characters per word
- `vocabulary_richness`: Unique words ratio
- `type_token_ratio`: Vocabulary diversity
- `hapax_ratio`: Ratio of words used only once
- `char_diversity`: Character variety
- `word_length_variance`: Word length consistency
- `unique_words_ratio`: Proportion of unique words
- `punctuation_ratio`: Punctuation usage
- `freq_*`: Letter frequency statistics

#### Syntactic Features
- `avg_sentence_length`: Words per sentence
- `sentence_complexity`: Structural complexity
- `avg_parse_tree_depth`: Sentence structure depth
- `parse_tree_breadth`: Phrase complexity
- `syntactic_diversity`: Sentence pattern variety
- `pos_*`: Part-of-speech distributions
- `dep_*`: Grammatical dependency patterns

#### Structural Features
- `avg_paragraph_length`: Words per paragraph
- `paragraph_length_variance`: Consistency
- `text_density`: Text vs. whitespace
- `structure_consistency`: Overall organization

#### Readability Features
- `flesch_reading_ease`: Standard readability (-100 to 100)
  - Higher scores = easier to read
- `gunning_fog`: Education level needed
- `smog_index`: Years of education needed
- `automated_readability_index`: US grade level

### 5. Recommendations
Actionable suggestions based on:
- Readability scores
- Structural analysis
- Vocabulary usage
- Sentence complexity
- Overall consistency

## Interpreting Results

### Good Writing Indicators
- Balanced complexity (30-70)
- High consistency (>0.7)
- Moderate sentence length
- Varied vocabulary
- Clear structure

### Areas for Improvement
- Very high complexity (>70)
- Low consistency (<0.3)
- Extreme readability scores
- Unbalanced metrics

## Using This Information
1. Focus on metrics that align with your target audience
2. Use recommendations to improve specific aspects
3. Track changes over multiple revisions
4. Compare against similar documents in your field 