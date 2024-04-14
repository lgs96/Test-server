import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description='Plot CWND and RTT from CSV files.')
parser.add_argument('subdir', type=str, help='Subdirectory name within the "result" folder')

# Parse arguments
args = parser.parse_args()

# Build the file path using the provided subdirectory argument
file_path = os.path.join('result', args.subdir, 'cwnd.csv')

# Check if the file exists
if not os.path.exists(file_path):
    print("File not found:", file_path)
else:
    # Load the data from CSV file
    df = pd.read_csv(file_path, header=None, names=['Time', 'CWND', 'RTT'], on_bad_lines='skip')

    # Try to convert 'Time' to numeric, coerce errors to NaN, then drop rows with NaN
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df.dropna(subset=['Time'], inplace=True)


    print('Min time: ', df['Time'].min())

    # Normalize the 'Time' column so that the first entry starts at 0
    min_time = df['Time'].min()
    df['Time'] = df['Time'] - min_time  # Subtracting min_time from all entries



    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot CWND
    plt.subplot(2, 1, 1)  # 2 rows, 1 column, 1st subplot
    plt.plot(df['Time'], df['CWND'], marker='o', color='b', label='CWND')
    plt.title('CWND and RTT over Time')
    plt.ylabel('CWND')
    plt.grid(True)
    plt.xticks(rotation=45)


    # Plot RTT
    plt.subplot(2, 1, 2)  # 2 rows, 1 column, 2nd subplot
    plt.plot(df['Time'], df['RTT'], marker='o', color='r', label='RTT')
    plt.xlabel('Time')
    plt.ylabel('RTT')
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()