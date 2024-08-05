# Ontology Alignment Using String Similarity Metrics

The `similarity-metrics.py` code compares attributes and values from TSV and TXT files to align ontology data. This procedure determines how closely linked the data in these files are by using various string similarity metrics. This README provides a detailed description of each step, the metrics used, and the criteria for evaluating results.

## Overview

The code performs the following main tasks:
1. **Reading Data**: Extracts attributes and values from TSV and TXT files.
2. **Calculating Similarity**: Utilizes different metrics to compare attributes and values.
3. **Finding Best Matches**: Identifies the best matches between data from TSV and TXT files.
4. **Saving Results**: Records the similarity results in CSV files for review.
5. **Handling Errors**: Tracks and reports files with issues.

## Detailed Steps

### 1. Reading Data

**Functions**: `read_tsv_attributes_values(file_path)` and `read_txt_attributes_values(file_path)`

- **Purpose**: Parses and organizes data into a structured format required for comparison. Extracts attributes and values from TSV and TXT files.
- **Relation to Paper**: Meaningful comparisons require accurate data extraction. Effective ontology alignment requires correctly formatted input, which is ensured by well-structured data. 

### 2. Calculating Similarity

**Functions**: `cosine_sim(str1, str2)`, fuzzy matching functions from the `fuzzywuzzy` library, and `jellyfish.jaro_winkler_similarity`.

- **Cosine Similarity**:
  - **Purpose**: Computes similarity based on the cosine of the angle between two TF-IDF vectors, reflecting term importance and occurrence.
  - **Relation to Paper**: Effective for comparing textual attributes by considering term frequency and importance, aiding in the alignment of attributes with varying term usage.

- **Fuzzy Matching**:
  - **Purpose**: Computes similarity ratios with the use of the `fuzzywuzzy` library, which allows for text typos and partial matches.
  - **Relation to Paper**: Critical for identifying similar attributes or values that may differ slightly due to typographical errors or inconsistent formatting.

- **Jaro-Winkler Similarity**:
  - **Purpose**: Measures similarity based on the Jaro-Winkler distance, useful for strings with common prefixes and minor typographical errors.
  - **Relation to Paper**: Good for matching attributes or values with minor text differences or similar roots.

### 3. Finding Best Matches

**Function**: `find_best_matches(tsv_data, txt_data)`

- **Purpose**: Compares all attributes and values from TSV and TXT files using the similarity metrics to identify the best matches between the triples.

### Evaluating Results

- **Good Results**: High similarity scores (e.g., cosine similarity close to 1, high fuzzy matching ratios, high Jaro-Winkler similarity) indicate strong alignment between attributes and values. Good results reflect well-matched pairs where the attributes or values are closely related or identical.
- **Interpreting Metrics**:
  - **Cosine Similarity**: Values close to 1 shows that the term vectors are highly similar, indicating strong alignment.
  - **Fuzzy Matching Ratios**: Higher ratios suggest that the strings are similar even with minor differences.
  - **Jaro-Winkler Similarity**: Values closer to 1 indicate strong similarity, particularly useful for strings with common prefixes.

**Note:** Adjust path if necesssary to replicate the code.