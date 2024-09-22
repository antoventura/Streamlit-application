import pandas as pd
import os

# Set the random seed for reproducibility
RANDOM_SEED = 42

# Set the maximum price (2 million euros)
MAX_PRICE = 2_000_000

def preprocess_data():
    # Load the original Excel file
    path = os.path.join(os.getcwd(), "Data/db_annunci_022022_CITTA_METROPOLITANA.xlsx")
    df = pd.read_excel(path)

    # Filter for Rome and houses with price <= 2 million euros
    rome_df = df[(df["CITTA"] == "Roma") & (df["PREZZO"] <= MAX_PRICE)]

    # Drop rows with missing values in essential columns
    rome_df = rome_df.dropna(subset=['LATITUDINE', 'LONGITUDINE', 'PREZZO'])

    # Randomly sample 5000 houses
    sampled_df = rome_df.sample(n=5000, random_state=RANDOM_SEED)

    # Save the sampled data to a new Excel file
    output_path = os.path.join(os.getcwd(), "Data/rome_houses_5000_sample.xlsx")
    sampled_df.to_excel(output_path, index=False)

    print(f"Sampled data saved to {output_path}")
    print(f"Number of houses in the sample: {len(sampled_df)}")

if __name__ == "__main__":
    preprocess_data()