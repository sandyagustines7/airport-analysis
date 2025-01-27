import pandas as pd
import glob
import os
import re


# Define output directory for intermediate files
output_directory = './processed_files'
os.makedirs(output_directory, exist_ok=True)

# Define columns to load
columns = [
    'FL_DATE', 'OP_CARRIER', 'ORIGIN', 'DEST',
    'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY',
    'CRS_ARR_TIME', 'ARR_TIME', 'ARR_DELAY',
    'CANCELLED', 'CANCELLATION_CODE', 'DIVERTED',
    'CARRIER_DELAY', 'WEATHER_DELAY',
    'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'
]

# Filter criteria 
origin_airports = ['LGA', 'EWR']

# Function to convert times into HH:MM format 
def convert_time(value):
    if pd.isna(value) or value == 0: 
        return None
    value = f"{int(value):04d}"
    return f"{value[:2]}:{value[2:]}"

# Function to extract the year from the filename
def extract_year_from_filename(filename):
    match = re.search(r'(\d{4})', filename)
    if match:
        return int(match.group(1))
    return None

# Process each CSV file separately
def process_file(file_path, output_directory):
    print(f'\nProcessing file: {file_path}')
    
    # Extract the year from the filename to set the date range
    year = extract_year_from_filename(file_path)
    if year is None:
        print(f"Could not determine the year from filename: {file_path}")

    # Set dynamic start and end dates based on the year
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')

    output_file = os.path.join(output_directory, f'{year}_processed.csv')

    with open(output_file, 'w') as f_out:
        for chunk in pd.read_csv(
            file_path, 
            chunksize=100000, 
            usecols=columns, 
            parse_dates=['FL_DATE'],
            header=0, 
            skip_blank_lines=True,
            encoding='utf-8'
        ):
            print(f'Chunk columns: {chunk.columns}')

            # Print the first few rows to inspect data
            print(f'First rows of chunk:\n{chunk.head()}')

            # Ensure FL_DATE is datetime
            chunk['FL_DATE'] = pd.to_datetime(chunk['FL_DATE'], errors='coerce')
            print(f"FL_DATE dtype after conversion: {chunk['FL_DATE'].dtype}")

            # Filter out rows with invalid dates
            chunk = chunk.dropna(subset=['FL_DATE'])

            # Convert str to datetime
            for time_col in ['DEP_TIME', 'ARR_TIME', 'CRS_DEP_TIME', 'CRS_ARR_TIME']:
                if time_col in chunk.columns:
                    chunk[time_col] = pd.to_datetime(
                        chunk['FL_DATE'].astype(str) + ' ' + chunk[time_col], errors='coerce'
        )

            # Convert delay columns to numeric and handle missing values
            delay_columns = [
                'DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 
                'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 
                'LATE_AIRCRAFT_DELAY'
            ]
            for col in delay_columns:
                if col in chunk.columns:
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0)

            # Check the number of rows before filtering
            print(f'Rows before filtering: {len(chunk)}')

            # Filter the data
            if {'ORIGIN', 'FL_DATE', 'DIVERTED', 'CANCELLED'}.issubset(chunk.columns):
                filtered_chunk = chunk[
                    (chunk['ORIGIN'].isin(origin_airports)) &
                    (chunk['FL_DATE'].between(start_date, end_date)) &
                    (chunk['DIVERTED'] == 0) &
                    (chunk['CANCELLED'] == 0)
                ]
                print(f'Rows after filtering: {len(filtered_chunk)}')
            else:
                print("Required columns missing in chunk")
                continue

            # Write filtered data to CSV
            filtered_chunk.to_csv(f_out, index=False, mode='a', header=f_out.tell() == 0)
    
    print(f'Processed data saved to {output_file}')
    

# Run the processing pipeline
def run_pipeline():
    csv_files = glob.glob('./*.csv')
    for file in csv_files:
        process_file(file, output_directory)

run_pipeline()







