import pandas as pd
import glob
import os

import pandas as pd
import glob
import os

# Define the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output directory
output_dir = os.path.join(script_dir, 'evaluation-report')

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Get all CSV files in the script directory
csv_files = glob.glob(os.path.join(script_dir, 'similarity_results_Enslaved*.csv'))

for file in csv_files:
    # Check if the file is empty or has no columns
    if os.path.getsize(file) == 0:
        print(f"Skipped empty file: {file}")
        continue

    try:
        # Read the CSV file
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        print(f"Skipped file with no data: {file}")
        continue

    # Group by the specified columns and aggregate by taking the maximum value of the similarity metrics
    if not df.empty:
        highest_values_df = df.groupby(['TSV Subject', 'TSV Predicate', 'TSV Value']).agg({
            'Predicate FuzzyWuzzy Ratio': 'max',
            'Predicate FuzzyWuzzy Token Set Ratio': 'max',
            'Predicate Jaro-Winkler Similarity': 'max',
            'Predicate Cosine Similarity': 'max',
            'Value FuzzyWuzzy Ratio': 'max',
            'Value FuzzyWuzzy Token Set Ratio': 'max',
            'Value Jaro-Winkler Similarity': 'max',
            'Value Cosine Similarity': 'max'
        }).reset_index()

       
        # Create the output file path
        output_file = os.path.join(output_dir, f'highest_values_Enslaved_{os.path.basename(file)}')

        # Save the aggregated data to a new CSV file
        highest_values_df.to_csv(output_file, index=False)

        print(f'Results saved to {output_file}')
