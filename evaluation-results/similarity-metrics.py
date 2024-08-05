from fuzzywuzzy import fuzz
import jellyfish
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os

# Read from the tsv files
def read_tsv_attributes_values(file_path):
    tsv_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                subject = parts[0].strip()
                predicate = parts[1].strip()
                obj = parts[2].strip()
                tsv_data.append((subject, predicate, obj))
    return tsv_data

# Read from the txt files
def read_txt_attributes_values(file_path):
    txt_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                parts = line.split(':', 1)
                predicate_value = parts[0].split('(')[0].strip()
                value = parts[1].strip()
                txt_data.append((predicate_value, value))
    return txt_data

# Function to calculate Cosine Similarity
def cosine_sim(str1, str2):
    vectors = [str1, str2]
    vectorizer = TfidfVectorizer()
    try:
        vector_matrix = vectorizer.fit_transform(vectors)
        if vector_matrix.shape[0] < 2:
            return 0.0  # Handle cases where a lot of things are missing
        vectors = vector_matrix.toarray()
        return cosine_similarity(vectors)[0][1]
    except ValueError:
        return 0.0  # Handle cases with whitespaces or empty rows

def find_best_matches(tsv_data, txt_data):
    matches = []
    for tsv_subject, tsv_predicate, tsv_obj in tsv_data:
        for txt_predicate, txt_obj in txt_data:
            # Comparison of predicates
            predicate_ratio = fuzz.ratio(tsv_predicate, txt_predicate)
            predicate_token_set_ratio = fuzz.token_set_ratio(tsv_predicate, txt_predicate)
            predicate_jw_similarity = jellyfish.jaro_winkler_similarity(tsv_predicate, txt_predicate)
            predicate_cosine = cosine_sim(tsv_predicate, txt_predicate)
            
            # Comparison of objects
            value_ratio = fuzz.ratio(tsv_obj, txt_obj)
            value_token_set_ratio = fuzz.token_set_ratio(tsv_obj, txt_obj)
            value_jw_similarity = jellyfish.jaro_winkler_similarity(tsv_obj, txt_obj)
            value_cosine = cosine_sim(tsv_obj, txt_obj)

            match = {
                'TSV Subject': tsv_subject,
                'TSV Predicate': tsv_predicate,
                'TSV Value': tsv_obj,
                'TXT Predicate': txt_predicate,
                'TXT Value': txt_obj,
                'Predicate FuzzyWuzzy Ratio': predicate_ratio,
                'Predicate FuzzyWuzzy Token Set Ratio': predicate_token_set_ratio,
                'Predicate Jaro-Winkler Similarity': predicate_jw_similarity,
                'Predicate Cosine Similarity': predicate_cosine,
                'Value FuzzyWuzzy Ratio': value_ratio,
                'Value FuzzyWuzzy Token Set Ratio': value_token_set_ratio,
                'Value Jaro-Winkler Similarity': value_jw_similarity,
                'Value Cosine Similarity': value_cosine
            }
            matches.append(match)
    return matches

# Directories containing TSV and TXT files
tsv_dir = './WikipediaData/MakingTSVs/Enslaved/EnslavedTSV/'
txt_dir = './Results/triples_GPT-4_WB/'

# Make sure we have them all
tsv_files = os.listdir(tsv_dir)
txt_files = os.listdir(txt_dir)

# Dictionary of file matches based on their names
file_matches = {}
issue_files = {'TSV': [], 'TXT': []}

# Find matching files (tsvs and txts)
for tsv_file in tsv_files:
    tsv_name = os.path.splitext(tsv_file)[0]
    best_match = None
    highest_ratio = 0
    for txt_file in txt_files:
        txt_name = os.path.splitext(txt_file)[0]
        ratio = fuzz.ratio(tsv_name, txt_name)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = txt_file
    if best_match:
        file_matches[tsv_file] = best_match
    else:
        issue_files['TSV'].append(tsv_file)

# For every tsv file that has a corresponding txt file
for tsv_file, txt_file in file_matches.items():
    tsv_path = os.path.join(tsv_dir, tsv_file)
    txt_path = os.path.join(txt_dir, txt_file)
    
    try:
        tsv_data = read_tsv_attributes_values(tsv_path)
        txt_data = read_txt_attributes_values(txt_path)

        matches = find_best_matches(tsv_data, txt_data)

        # Output to CSV for each pair
        output_file = f'similarity_results_{os.path.splitext(tsv_file)[0]}.csv'
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=matches[0].keys())
            writer.writeheader()
            writer.writerows(matches)

        print(f"Similarity results for {tsv_file} and {txt_file} have been saved to {output_file}")
    
    except Exception as e:
        print(f"An issue occurred with files {tsv_file} and {txt_file}: {e}")
        issue_files['TXT'].append(txt_file)

# Print files with issues
#print("Files with issues:")
#print("TSV Files:", issue_files['TSV'])
#print("TXT Files:", issue_files['TXT'])
