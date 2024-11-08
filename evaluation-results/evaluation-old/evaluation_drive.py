from fuzzywuzzy import fuzz
import jellyfish
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os
import argparse

from google.colab import drive
drive.mount('https://drive.google.com/drive/folders/143sD_vRaBpA3-IuVlC160mw8TEWIbDZB')

# Function to read TSV attributes and values
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

# Function to read triples from the TXT file
def read_triples_txt(file_path):
    triples = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line and '(' in line and ')' in line:
                parts = line.strip().split(':', 1)
                predicate, values = parts[0].strip(), parts[1].strip()
                subject, obj = values.split('(', 1)[-1].split(',', 1)
                subject = subject.strip()
                obj = obj.replace(')', '').strip()
                triples.append((subject, predicate, obj))
    return triples

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
        for txt_subject, txt_predicate, txt_obj in txt_data:
            if tsv_subject != txt_subject:
                continue  # Only compare triples with the same subject

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

def main(tsv_dir, txt_dir, output_dir):
    # Make sure we have all files
    tsv_files = os.listdir(tsv_dir)
    txt_files = os.listdir(txt_dir)

    # Dictionary of file matches based on their names
    file_matches = {}

    # Find matching files (TSVs and TXT triples)
    for tsv_file in tsv_files:
        tsv_name = os.path.splitext(tsv_file)[0]
        best_match = None
        highest_ratio = 0
        for txt_file in txt_files:
            if '_triples' in txt_file:  # Only consider _triples.txt files
                txt_name = os.path.splitext(txt_file)[0].replace('_triples', '')
                ratio = fuzz.ratio(tsv_name, txt_name)
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = txt_file
        if best_match:
            file_matches[tsv_file] = best_match

    # For every TSV file that has a corresponding TXT file
    for tsv_file, txt_file in file_matches.items():
        tsv_path = os.path.join(tsv_dir, tsv_file)
        txt_path = os.path.join(txt_dir, txt_file)
        
        try:
            tsv_data = read_tsv_attributes_values(tsv_path)
            txt_data = read_triples_txt(txt_path)

            matches = find_best_matches(tsv_data, txt_data)

            # Output to CSV for each pair
            output_file = os.path.join(output_dir, f'similarity_results_{os.path.splitext(tsv_file)[0]}.csv')
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=matches[0].keys())
                writer.writeheader()
                writer.writerows(matches)

            print(f"Similarity results for {tsv_file} and {txt_file} have been saved to {output_file}")
        
        except Exception as e:
            print(f"An issue occurred with files {tsv_file} and {txt_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate TSV files against TXT triples.')
    parser.add_argument('--tsv_dir', type=str, required=True, help='Directory containing TSV files')
    parser.add_argument('--txt_dir', type=str, required=True, help='Directory containing TXT triples files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output CSV files')

    args = parser.parse_args()

    main(args.tsv_dir, args.txt_dir, args.output_dir)
