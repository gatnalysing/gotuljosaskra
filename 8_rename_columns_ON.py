import re

# Define a mapping of specific renames you want to apply
specific_rename_map = {
    "Heimtaugarskápur XID": "Heimtaugarskápur_XID",
    "Ljósastaur XID": "Ljósastaur_XID",
    "Tegund viðfangs": "Tegund_viðfangs",
    "Dags. uppsett": "Dags_uppsett",
    "Eigandi 2": "Eigandi_2",
    "Eigandi Umsjón-starfsmaður": "Eigandi_Umsjón_starfsmaður",
    "Kennitala eiganda": "Kennitala_eiganda",
    "Hæð staurs [m]": "Hæð_staurs_m"
}

def normalize_column_name(column_name):
    """
    Normalizes column names by replacing spaces and special characters with underscores.
    Specific renames are handled via a rename map.
    """
    # Check if the column name is in the specific rename map
    if column_name in specific_rename_map:
        return specific_rename_map[column_name]

    # General normalization: replace spaces and special characters
    normalized_name = re.sub(r'[ .\[\]]', '_', column_name)
    return normalized_name

# Example list of column names from the PRAGMA output
column_names = [
    "Heimtaugarskápur XID",
    "Heimtaugarskápur",
    "Ljósastaur XID",
    "Gata",
    "Staðsetning",
    "Tegund viðfangs",
    "Undirtegund",
    "X",
    "Y",
    "Dags. uppsett",
    "Eigandi 2",
    "Eigandi Umsjón-starfsmaður",
    "Kennitala eiganda",
    "Hæð staurs [m]"
]

# Apply normalization
renamed_columns = [normalize_column_name(col) for col in column_names]

# Print out the original and renamed columns for comparison
for original, renamed in zip(column_names, renamed_columns):
    print(f"Original: {original} -> Renamed: {renamed}")
