import re
import os
import pandas as pd

# Variable with the path to the main folder containing subfolders
main_folder_path = "/home/vinicius/Dev/flow-release/rocprof/rocprof-outputs"  
# List with the phrases that precede the number
phrase_list = ["Simulation time:", "Peaceman calc. time:", "Stdw computePerfRate time:", "Stdw apply time:", "GPU Stdw apply time:", "     Stdw apply counter:", "     GPU Stdw apply counter:", "Msw rate calc. time:", "Msw computePerfRate time:", "Msw apply time:",  "     Msw apply counter:", "       Msw data transfer time:"]

profile_count = [ "     GPU Stdw apply counter:"]
profile_value = [ "GPU Stdw apply time:"]

# List with the column headers    
column_headers = ["File Name", "Simulation Time", "STDW Rate Calculation Time", "STDW computePerfRate Time", "STDW Apply Time",  "GPU STDW Apply Time", "STDW Apply Number of Calls", "GPU STDW Apply Number of Calls", "MSW Rate Calulation Time", "MSW computePerfRate Time", "MSW Apply Time", "MSW Apply Number of Calls", "MSW Data Transfer Time"]

# Int variables for the CSV column indexes
kernel_column_index = 0  # Column to check for the correspondence string
value_column_index = 1  # Column to extract the value from

count_column_index = 13 # Column to count the number of incidences of the kernel string

# The string that should be matched for correspondence in the CSV files
kernel_string = "void Opm::stdwell_apply<double>(double const*, double const*, double const*, unsigned int const*, unsigned int const*, double const*, double*, unsigned int, unsigned int, unsigned int const*) (.kd)"

# Function to get the data from a file based on a specific phrase
def extract_value(file_name, phrase):
    try:
        with open(file_name, "r") as file:
            for line in file:
                if phrase in line:
                    match = re.search(r'{}[^\d]*([\d.]+)'.format(re.escape(phrase)), line)
                    if match:
                        return float(match.group(1))
        return -1  # Return -1 if no value is found
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return -1

# Function to count the number of incidences of a string in a specific column of a CSV file
def count_kernel_in_csv(folder_path, kernel_string, kernel_col_idx):
    csv_file_name = None
    for file in os.listdir(folder_path):
        if file.startswith("results_NORNE") and file.endswith(".csv"):
            csv_file_name = file
            break
    
    if csv_file_name is None:
        return -1  # No CSV file found
    
    csv_file_path = os.path.join(folder_path, csv_file_name)
    
    try:
        df = pd.read_csv(csv_file_path)
        count = df.iloc[:, kernel_col_idx].tolist().count(kernel_string)
        return count
    except Exception as e:
        print(f"Error reading CSV file {csv_file_path}: {e}")
        return 0

def extract_value_from_results_stats_csv(folder_path, kernel_string, kernel_col_idx, value_col_idx):
    results_stats_csv_file_name = None
    for file in os.listdir(folder_path):
        if file.startswith("results_stat") and file.endswith(".csv"):
            results_stats_csv_file_name = file
            break
    
    if results_stats_csv_file_name is None:
        print("No results_stats CSV file found.")
        return -1
    
    results_stats_csv_file_path = os.path.join(folder_path, results_stats_csv_file_name)
    
    try:
        df = pd.read_csv(results_stats_csv_file_path)
        if kernel_col_idx >= len(df.columns) or value_col_idx >= len(df.columns):
            raise ValueError(f"Column index {kernel_col_idx} or {value_col_idx} out of bounds.")
        match = df[df.iloc[:, kernel_col_idx] == kernel_string]
        if not match.empty:
            return match.iloc[0, value_col_idx]
        return -1
    except Exception as e:
        print(f"Error reading results_stats CSV file {results_stats_csv_file_path}: {e}")
        return -1


# Nested loop to iterate through the folder structure, find files, and extract values
table_data = []
for root, dirs, files in os.walk(main_folder_path):
    # Skip the "backup" and "experiments" folders
    dirs[:] = [d for d in dirs if not d.startswith("experiment") and d != "backup"]
    
    for file in files:
        if file.endswith("output.txt"):
            full_file_path = os.path.join(root, file)
            folder_path = root
            row = []
            # Extract the file name without the extension
            file_name_without_ext = os.path.splitext(os.path.basename(full_file_path))[0]
            row.append(file_name_without_ext)
            
            # Extract values for phrases related to .txt files
            for phrase in phrase_list:
                value = extract_value(full_file_path, phrase)
                
                # If the phrase is "critical-phrase" and value is zero, count incidences in the CSV file
                if phrase in profile_count:
                    value = count_kernel_in_csv(folder_path, kernel_string, count_column_index)

                if phrase in profile_value:
                    value = extract_value_from_results_stats_csv(folder_path, kernel_string, kernel_column_index, value_column_index)
                row.append(value)
            
            # Add the row to the table_data
            table_data.append(row)

# Create the DataFrame
if table_data:
    df = pd.DataFrame(table_data, columns=column_headers)
    # Sort the DataFrame by the first column
    df = df.sort_values(by="File Name")
    # Save the DataFrame as a CSV file
    csv_file_path = "summarize-table.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"Table saved as '{csv_file_path}'")
else:
    print("No data found to populate the table.")
