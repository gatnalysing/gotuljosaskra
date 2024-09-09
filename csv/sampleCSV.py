import os
import csv

# Define the output file
output_file = "sample.txt"

# Open the output file in write mode
with open(output_file, "w") as output:
    # Loop through all files in the current directory
    for file_name in os.listdir("."):
        # Process only CSV files
        if file_name.endswith(".csv"):
            output.write(f"{file_name}\n")
            with open(file_name, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                # Write the first 3 lines of each CSV file to the output file
                for i, row in enumerate(csv_reader):
                    if i < 3:
                        output.write(",".join(row) + "\n")
                    else:
                        break
            output.write("\n")

print(f"Sampled CSV data has been written to {output_file}")
