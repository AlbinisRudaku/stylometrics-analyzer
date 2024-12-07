# Stilo Metrics Guide

## Understanding Your Results

### 1. Metadata
- `filename`: The name of your document
- `file_size`: How big your file is in bytes (larger numbers mean bigger files)
- `page_count`: How many pages are in your document
- `timestamp`: When the analysis was done

### 2. Style Metrics

#### Complexity Score (0-100)
What it means: How difficult your text is to read
- 0-30: Very easy to read
- 30-50: Moderately easy
- 50-70: Somewhat difficult
- 70-100: Very difficult

Your score components:
- `vocabulary_contribution`: How much difficult words affect the score
- `syntax_contribution`: How much sentence structure affects the score
- `readability_contribution`: How much overall readability affects the score

Example: If you see "complexity.score: 75", your text is quite difficult to read

#### Consistency Score (0-1)
What it means: How similar your writing style stays throughout the document
- 0-0.3: Very inconsistent
- 0.3-0.7: Somewhat consistent
- 0.7-1.0: Very consistent

Example: A score of 0.2 means your writing style changes a lot throughout the text

### 3. Writing Patterns

#### Vocabulary Usage
- "Advanced": You use many complex or uncommon words
- "Moderate": You use a mix of simple and complex words
- "Basic": You mostly use common, simple words

#### Sentence Structure
- "Complex": You write long sentences with many parts
- "Varied": You mix short and long sentences
- "Simple": You write short, straightforward sentences

#### Text Organization
- "Well Structured": Your paragraphs flow logically
- "Moderately Structured": Some organization but could be clearer
- "Loosely Structured": Needs better organization

### 4. Detailed Measurements

#### Word Usage (Lexical Features)
- `avg_word_length`: Average length of your words
  - Below 4: Very simple words
  - 4-5: Normal
  - Above 5: Complex words

- `vocabulary_richness`: How many different words you use (0-1)
  - 0-0.3: Limited vocabulary
  - 0.3-0.6: Good variety
  - 0.6-1.0: Extensive vocabulary

- `hapax_ratio`: Words used only once (0-1)
  - Higher numbers mean more unique words

- `word_length_variance`: How consistent your word lengths are
  - Lower numbers mean more consistent word lengths

#### Sentence Analysis (Syntactic Features)
- `avg_sentence_length`: Words per sentence
  - 10-15: Very easy to read
  - 15-20: Standard
  - Above 20: Complex

- `sentence_complexity`: How complicated your sentences are
  - Below 30: Simple sentences
  - 30-50: Normal complexity
  - Above 50: Very complex

#### Document Structure
- `avg_paragraph_length`: Words in each paragraph
  - 50-100: Easy to read
  - 100-200: Standard
  - Above 200: Very dense

- `text_density`: How packed with text your document is (0-1)
  - Higher numbers mean less whitespace

#### Readability Scores
- `flesch_reading_ease` (-100 to 100):
  - 90-100: Very easy (5th grade)
  - 60-70: Standard (8th-9th grade)
  - Below 30: Very difficult (college level)

- `gunning_fog`: Years of education needed to understand
  - 6: Sixth grade
  - 12: High school
  - 16: College graduate

### 5. What Your Results Mean

Looking at your specific results:
- Complexity score of 25.37: Your text is moderately complex
- Consistency score of 0: Your writing style varies significantly
- Very low readability scores: The text is extremely difficult to read
- High sentence complexity (59.0): Your sentences are very complex
- Average word length of 4.92: You use slightly longer words than average

### 6. How to Improve Your Writing

Based on these metrics:
1. Break long sentences into shorter ones
2. Use simpler words where possible
3. Make paragraph lengths more consistent
4. Add more structure with headings and transitions
5. Try to maintain a more consistent writing style throughout

### 7. When to Use Different Styles

Academic Writing:
- Higher complexity is okay (40-70)
- Longer sentences acceptable
- Technical vocabulary expected

General Reading:
- Aim for lower complexity (20-40)
- Shorter sentences
- Simpler vocabulary

Business Writing:
- Medium complexity (30-50)
- Clear, direct sentences
- Professional but accessible vocabulary