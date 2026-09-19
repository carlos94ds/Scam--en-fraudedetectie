"""
Vervolg op de baseline: Logistic Regression op URL-only + website-kenmerken
samen, om te vergelijken met het URL-only baseline-resultaat.

De website-kenmerken komen hier uit de dataset zelf (al eerder door de
dataset-makers berekend). In de webapplicatie berekent src/website_features.py
dezelfde soort kenmerken live, door de opgegeven website te bezoeken; de
TLD- en Robots-categorieën die hier tijdens trainen zijn gebruikt, worden
daarom ook opgeslagen (url_website_vocab.json), zodat live-inferentie exact
dezelfde one-hot-kolommen reconstrueert als tijdens trainen.
"""
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
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

from src.feature_lists import URL_ONLY_FEATURES, WEBSITE_FEATURES, LABEL_COLUMN

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
RANDOM_STATE = 42


def build_features(df, feature_list):
    """Retourneert (X, vocab) waarbij vocab de categorieën vastlegt die voor
    TLD en Robots zijn gebruikt (top-20 TLD's + "overig", en alle geziene
    Robots-waarden). Die vocab wordt apart opgeslagen zodat live-inferentie
    in de webapp (src/website_features.py) precies dezelfde one-hot-kolommen
    kan reconstrueren voor een nieuwe, niet eerder geziene URL."""
    X = df[feature_list].copy()
    vocab = {"tld": [], "robots": []}

    # Title is vrije tekst (de titel van de webpagina) - geen bruikbaar
    # numeriek/categorisch kenmerk zonder aparte tekstverwerking (NLP).
    # We laten 'm hier weg; DomainTitleMatchScore en URLTitleMatchScore
    # vangen de relevante informatie (of de titel bij het domein past) al
    # wel numeriek op.
    if "Title" in X.columns:
        X = X.drop(columns=["Title"])

    if "TLD" in X.columns:
        top_tlds = X["TLD"].value_counts().nlargest(20).index
        vocab["tld"] = list(top_tlds)
        X["TLD"] = X["TLD"].where(X["TLD"].isin(top_tlds), other="overig")
        X = pd.get_dummies(X, columns=["TLD"], prefix="TLD")

    # Robots is ook tekstueel/categorisch van aard in deze dataset - one-hot
    # encoderen net als TLD.
    if "Robots" in X.columns and X["Robots"].dtype == object:
        vocab["robots"] = sorted(X["Robots"].dropna().unique().tolist())
        X = pd.get_dummies(X, columns=["Robots"], prefix="Robots")

    return X, vocab


def evaluate(name, X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    print(f"\n=== {name} ===")
    print(f"Aantal features: {X.shape[1]}")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1-score:  {f1_score(y_test, y_pred):.4f}")

    # cross-validation ter controle, net als bij de baseline
    X_scaled_full = StandardScaler().fit_transform(X)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X_scaled_full, y, cv=cv, scoring="accuracy")
    print(f"Cross-val accuracy: {cv_scores.mean():.4f} (std: {cv_scores.std():.4f})")

    print("\nClassificatierapport:")
    print(classification_report(y_test, y_pred, target_names=["Phishing", "Legitiem"]))

    coef_df = pd.DataFrame({
        "feature": X.columns,
        "coefficient": model.coef_[0],
    }).sort_values("coefficient", key=abs, ascending=False)
    print("Top 10 belangrijkste kenmerken:")
    print(coef_df.head(10).to_string(index=False))

    return model, scaler, X.columns, accuracy_score(y_test, y_pred), f1_score(y_test, y_pred)


def main():
    df = pd.read_csv(DATA_PATH)
    y = df[LABEL_COLUMN]

    # --- Model A: alleen URL (ter vergelijking, nu met dezelfde CV-toevoeging) ---
    X_url_only, _ = build_features(df, URL_ONLY_FEATURES)
    _, _, _, acc_url, f1_url = evaluate("Model A: URL-only (baseline)", X_url_only, y)

    # --- Model B: URL + website-kenmerken samen ---
    combined_features = URL_ONLY_FEATURES + WEBSITE_FEATURES
    X_combined, vocab = build_features(df, combined_features)
    model_b, scaler_b, columns_b, acc_combined, f1_combined = evaluate(
        "Model B: URL + website-kenmerken", X_combined, y
    )

    # --- Vergelijking ---
    print("\n=== Vergelijking ===")
    print(f"Model A (URL-only):          accuracy {acc_url:.4f}, F1 {f1_url:.4f}")
    print(f"Model B (URL + website):     accuracy {acc_combined:.4f}, F1 {f1_combined:.4f}")
    print(f"Verschil in accuracy: {acc_combined - acc_url:+.4f}")

    # --- Opslaan van model B ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model_b, os.path.join(MODEL_DIR, "url_website_logreg.pkl"))
    joblib.dump(scaler_b, os.path.join(MODEL_DIR, "url_website_scaler.pkl"))
    joblib.dump(list(columns_b), os.path.join(MODEL_DIR, "url_website_feature_columns.pkl"))
    with open(os.path.join(MODEL_DIR, "url_website_vocab.json"), "w") as f:
        json.dump(vocab, f, indent=2)
    print(f"\nModel B, scaler en vocab (TLD/Robots-categorieën) opgeslagen in: {MODEL_DIR}")


if __name__ == "__main__":
    main()
