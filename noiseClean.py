import pandas as pd
import numpy as np
import string
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AVAILABLE_CHARS = set(string.digits + string.ascii_letters + string.punctuation)
logging.info(f"Available characters: {AVAILABLE_CHARS}")

def is_string_valid(input_string):
    """Check if all characters in the string are valid."""
    return input_string if all(char in AVAILABLE_CHARS for char in input_string) else np.nan


'''
def process_file(file, input_dir, output_dir, colnames):
    """Process a single file to clean noise and save the result in chunks."""
    filename = file.replace('.csv', '.pickle')
    output_path = os.path.join(output_dir, filename)
    
    # 이미 처리된 파일이 존재하는 경우 스킵
    if os.path.exists(output_path):
        logging.info(f"File already exists. Skipping: {output_path}")
        return

    input_path = os.path.join(input_dir, file)
    logging.info(f"Processing file: {input_path}")

    try:
        chunk_size = 100000  # 한 번에 처리할 행의 수
        for chunk in pd.read_csv(input_path, names=colnames, header=None, chunksize=chunk_size):
            chunk = chunk.dropna()
            for column in colnames:
                chunk[column] = chunk[column].apply(is_string_valid)
                chunk = chunk.dropna(subset=[column])
            # 기존 데이터프레임에 추가 저장
            if os.path.exists(output_path):
                existing_data = pd.read_pickle(output_path)
                combined_data = pd.concat([existing_data, chunk])
                combined_data.to_pickle(output_path)
            else:
                chunk.to_pickle(output_path)
    except Exception as e:
        logging.error(f"Error processing {input_path}: {e}")

    logging.info(f"Saved cleaned data to: {output_path}\n")
'''

def process_file(file, input_dir, output_dir, colnames):
    """Process a single file to clean noise and save the result."""
    filename = file.replace('.csv', '.pickle')
    output_path = os.path.join(output_dir, filename)
    
    # 이미 처리된 파일이 존재하는 경우 스킵
    if os.path.exists(output_path):
        logging.info(f"File already exists. Skipping: {output_path}")
        return

    input_path = os.path.join(input_dir, file)
    logging.info(f"Processing file: {input_path}")

    try:
        data = pd.read_csv(input_path, names=colnames, header=None)
    except Exception as e:
        logging.error(f"Error reading {input_path}: {e}")
        return

    logging.info(f"Original length: {len(data)}")
    data = data.dropna()
    logging.info(f"Length after NaN removal: {len(data)}")

    for column in colnames:
        data[column] = data[column].apply(is_string_valid)
        data = data.dropna(subset=[column])
        logging.info(f"Length after {column} noise removal: {len(data)}")

    data.to_pickle(output_path)
    logging.info(f"Saved cleaned data to: {output_path}\n")



def display_cleaned_file_sizes(file, output_dir):
    """Display the sizes of all cleaned files."""
    filename = file.replace('.csv', '.pickle')
    path = os.path.join(output_dir, filename)
    try:
        data = pd.read_pickle(path)
        logging.info(f"{filename}: {len(data)}")
    except Exception as e:
        logging.error(f"Error reading {path}: {e}")

def main():
    input_dir = './passdata/temp/'  # Adjusted based on your path
    output_dir = './NoiseCleaned/'
    colnames = ['ID', 'Domain', 'PW']

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each file
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            process_file(file, input_dir, output_dir, colnames)
    
    # Display the sizes of the cleaned files
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            display_cleaned_file_sizes(file, output_dir)

if __name__ == '__main__':
    main()
