"""
Baseline-model: Logistic Regression op alleen de URL-only kenmerken.

Doel van deze stap: een eerste werkend model dat we later kunnen vergelijken
met de uitgebreide versie (URL + website-kenmerken, fase 2).
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from src.feature_lists import URL_ONLY_FEATURES, LABEL_COLUMN

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
RANDOM_STATE = 42  # vaste seed, zodat de split en dus de resultaten reproduceerbaar zijn


def main():
    df = pd.read_csv(DATA_PATH)

    # --- Features en label scheiden ---
    X = df[URL_ONLY_FEATURES].copy()
    y = df[LABEL_COLUMN]

    # TLD is tekst (bijv. "com", "nl"), geen getal. We zetten 'm om naar losse
    # 0/1-kolommen per TLD (one-hot encoding), zodat het model ermee kan rekenen.
    # We beperken dit tot de 20 meest voorkomende TLD's; de rest valt in "overig",
    # anders krijgen we honderden kolommen voor zeldzame TLD's die het model
    # nauwelijks vaker dan een paar keer ziet.
    top_tlds = X["TLD"].value_counts().nlargest(20).index
    X["TLD"] = X["TLD"].where(X["TLD"].isin(top_tlds), other="overig")
    X = pd.get_dummies(X, columns=["TLD"], prefix="TLD")

    # --- Train/test-split ---
    # We houden 20% apart als testset die het model nooit ziet tijdens trainen.
    # stratify=y zorgt dat de verhouding phishing/legitiem in beide sets gelijk
    # blijft aan de originele dataset (57%/43%).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Trainset: {X_train.shape[0]} rijen, Testset: {X_test.shape[0]} rijen")

    # --- Schalen ---
    # Logistic Regression werkt beter als alle kenmerken op een vergelijkbare
    # schaal staan (bijv. URLLength loopt tot 6097, IsHTTPS is 0 of 1). We
    # fitten de scaler alleen op de trainset, en passen 'm daarna toe op beide
    # sets, zodat er geen informatie van de testset "lekt" naar het trainen.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- Model trainen ---
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)

    # --- Evalueren ---
    y_pred = model.predict(X_test_scaled)

    print("\n--- Resultaten op de testset ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1-score:  {f1_score(y_test, y_pred):.4f}")

    print("\n--- Confusion matrix ---")
    print("             Voorspeld phishing | Voorspeld legitiem")
    cm = confusion_matrix(y_test, y_pred)
    print(f"Echt phishing:      {cm[0][0]:>6}          | {cm[0][1]:>6}")
    print(f"Echt legitiem:      {cm[1][0]:>6}          | {cm[1][1]:>6}")

    print("\n--- Classificatierapport ---")
    print(classification_report(y_test, y_pred, target_names=["Phishing", "Legitiem"]))

    # --- Belangrijkste kenmerken ---
    # Bij Logistic Regression is de coefficient direct te interpreteren: hoe
    # groter (in absolute waarde), hoe sterker dat kenmerk meeweegt in de
    # beslissing. Een positieve coefficient duwt richting "legitiem" (label 1).
    coef_df = pd.DataFrame({
        "feature": X.columns,
        "coefficient": model.coef_[0],
    }).sort_values("coefficient", key=abs, ascending=False)

    print("\n--- Top 10 belangrijkste kenmerken (grootste |coefficient|) ---")
    print(coef_df.head(10).to_string(index=False))

    # --- Opslaan ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "baseline_logreg.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "baseline_scaler.pkl"))
    joblib.dump(list(X.columns), os.path.join(MODEL_DIR, "baseline_feature_columns.pkl"))
    print(f"\nModel en scaler opgeslagen in: {MODEL_DIR}")


if __name__ == "__main__":
    main()
