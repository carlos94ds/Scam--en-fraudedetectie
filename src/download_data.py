"""
Downloadt de PhiUSIIL Phishing URL Dataset van UCI en slaat 'm op als CSV in data/.

Bron: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
Licentie: CC BY 4.0 (Prasad & Chandra, 2024)
"""
import os
from ucimlrepo import fetch_ucirepo
import pandas as pd

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")


def main():
    print("Dataset ophalen van UCI...")
    dataset = fetch_ucirepo(id=967)

    X = dataset.data.features
    y = dataset.data.targets

    df = pd.concat([X, y], axis=1)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset opgeslagen: {OUTPUT_PATH}")
    print(f"Aantal rijen: {len(df)}")
    print(f"Aantal kolommen: {len(df.columns)}")
    print("\nEerste kolommen:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()
