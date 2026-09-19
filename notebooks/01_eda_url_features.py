"""
Eerste verkenning (EDA) van de PhiUSIIL-dataset, beperkt tot de URL-only
kenmerken die bij onze MVP horen. URLSimilarityIndex is bewust uitgesloten,
zie docs/data-decisions.md.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import matplotlib.pyplot as plt

from src.feature_lists import URL_ONLY_FEATURES, LABEL_COLUMN

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")


def main():
    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")

    # --- Klassenbalans ---
    print("\n--- Klassenbalans (1 = legitiem, 0 = phishing) ---")
    counts = df[LABEL_COLUMN].value_counts()
    percentages = df[LABEL_COLUMN].value_counts(normalize=True) * 100
    for klasse in counts.index:
        print(f"Label {klasse}: {counts[klasse]} rijen ({percentages[klasse]:.1f}%)")

    counts.sort_index().plot(kind="bar", color=["#c0392b", "#27ae60"])
    plt.xticks([0, 1], ["Phishing (0)", "Legitiem (1)"], rotation=0)
    plt.title("Klassenbalans")
    plt.ylabel("Aantal URL's")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "class_balance.png"))
    plt.close()

    # --- Ontbrekende waarden ---
    print("\n--- Ontbrekende waarden (URL-only kolommen) ---")
    missing = df[URL_ONLY_FEATURES].isnull().sum()
    missing = missing[missing > 0]
    print(missing if len(missing) else "Geen ontbrekende waarden gevonden.")

    # --- Beschrijvende statistiek ---
    print("\n--- Beschrijvende statistiek (URL-only, numeriek) ---")
    numeric_cols = df[URL_ONLY_FEATURES].select_dtypes(include="number").columns
    print(df[numeric_cols].describe().T[["mean", "std", "min", "max"]])

    # --- Samenhang met het label ---
    print("\n--- Correlatie met label, gesorteerd (URL-only, numeriek) ---")
    correlaties = df[list(numeric_cols) + [LABEL_COLUMN]].corr()[LABEL_COLUMN].drop(LABEL_COLUMN)
    correlaties = correlaties.sort_values(key=abs, ascending=False)
    print(correlaties)

    plt.figure(figsize=(8, 10))
    correlaties.plot(kind="barh")
    plt.title("Correlatie van URL-only kenmerken met label\n(URLSimilarityIndex uitgesloten, zie docs/data-decisions.md)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "correlation_with_label.png"))
    plt.close()

    # --- Voorbeeld: verdeling van URLLength per klasse ---
    df.boxplot(column="URLLength", by=LABEL_COLUMN)
    plt.title("URLLength per klasse")
    plt.suptitle("")
    plt.xlabel("Label (0 = phishing, 1 = legitiem)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "urllength_by_label.png"))
    plt.close()

    print(f"\nFiguren opgeslagen in: {FIG_DIR}")


if __name__ == "__main__":
    main()
