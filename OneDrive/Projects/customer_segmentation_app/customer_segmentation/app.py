import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_PATH  = os.path.join(os.path.dirname(__file__), "kmeans_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

scaler = None
if os.path.exists(SCALER_PATH):
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

# ── Cluster metadata ──────────────────────────────────────────────────────────
CLUSTER_INFO = {
    0: {
        "name": "At-Risk Customers",
        "emoji": "⚠️",
        "color": "#f97316",
        "description": (
            "Previously engaged buyers who haven't purchased recently. "
            "They have moderate purchase history but high recency — "
            "re-engagement campaigns and personalised offers can win them back."
        ),
        "tags": ["Low Spending", "High Recency", "Needs Re-engagement"],
    },
    1: {
        "name": "Window Shoppers",
        "emoji": "🛍️",
        "color": "#6366f1",
        "description": (
            "Frequent visitors with above-average income who browse often "
            "but convert less. High web activity with moderate spend — "
            "targeted promotions and urgency nudges can convert intent into sales."
        ),
        "tags": ["High Web Visits", "Moderate Income", "Low Conversion"],
    },
    2: {
        "name": "Budget Buyers",
        "emoji": "💰",
        "color": "#22c55e",
        "description": (
            "Value-conscious customers who buy frequently but spend modestly. "
            "Recent purchasers with high purchase counts — "
            "loyalty rewards and bundle deals keep them active and grow basket size."
        ),
        "tags": ["High Frequency", "Low Spend", "Recent Buyers"],
    },
    3: {
        "name": "VIP Customers",
        "emoji": "👑",
        "color": "#eab308",
        "description": (
            "High-income, high-spending top-tier customers with premium purchase patterns. "
            "Low recency (they buy often) and large transaction values — "
            "exclusive perks, early access, and premium support maximise retention."
        ),
        "tags": ["High Income", "High Spending", "Top Tier"],
    },
}

# ── Fallback manual scaling (used when no scaler.pkl is present) ──────────────
# These are typical ranges for a marketing / CRM customer dataset.
FEATURE_STATS = {
    #           mean,   std
    "Income":   (52000,  28000),
    "Age":      (44,     13),
    "Recency":  (49,     29),
    "Spending": (600,    400),
    "Purchases":(14,     8),
    "WebVisits":(5,      3),
}

FEATURE_ORDER = list(FEATURE_STATS.keys())


def scale_input(values: list[float]) -> np.ndarray:
    """Scale raw inputs using loaded scaler or fallback z-score."""
    arr = np.array(values, dtype=float).reshape(1, -1)
    if scaler is not None:
        return scaler.transform(arr)
    # Manual z-score normalisation
    means = np.array([FEATURE_STATS[f][0] for f in FEATURE_ORDER], dtype=float)
    stds  = np.array([FEATURE_STATS[f][1] for f in FEATURE_ORDER], dtype=float)
    return (arr - means) / stds


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    try:
        features = [
            float(data["income"]),
            float(data["age"]),
            float(data["recency"]),
            float(data["spending"]),
            float(data["purchases"]),
            float(data["webvisits"]),
        ]
    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400

    scaled    = scale_input(features)
    cluster   = int(model.predict(scaled)[0])
    info      = CLUSTER_INFO[cluster]

    return jsonify({
        "cluster": cluster,
        "name":        info["name"],
        "emoji":       info["emoji"],
        "color":       info["color"],
        "description": info["description"],
        "tags":        info["tags"],
    })


if __name__ == "__main__":
    app.run(debug=True)
