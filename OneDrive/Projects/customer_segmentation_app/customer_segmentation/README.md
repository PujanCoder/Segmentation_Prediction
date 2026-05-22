# 🧠 Customer Segmentation · AI Classifier

A Flask web application that classifies customers into behavioural segments using a pre-trained **K-Means clustering model** (4 clusters, 6 features).

## Segments

| Cluster | Name | Description |
|---------|------|-------------|
| 0 | ⚠️ At-Risk Customers | Previously engaged buyers who haven't purchased recently |
| 1 | 🛍️ Window Shoppers | Frequent browsers with moderate income but low conversion |
| 2 | 💰 Budget Buyers | Value-conscious, high-frequency, low-spend customers |
| 3 | 👑 VIP Customers | High-income, high-spending premium customers |

## Features Used

| Feature | Description | Typical Range |
|---------|-------------|---------------|
| `income` | Annual household income (USD) | 0 – 200,000 |
| `age` | Customer age (years) | 18 – 100 |
| `recency` | Days since last purchase | 0 – 365 |
| `spending` | Total spend in the past year (USD) | 0 – 2,500+ |
| `purchases` | Number of purchases made | 0 – 50 |
| `webvisits` | Web visits per month | 0 – 20 |

## Project Structure

```
customer_segmentation/
├── app.py                  # Flask backend — model loading + /predict API
├── kmeans_model.pkl        # Pre-trained K-Means model
├── scaler.pkl              # (optional) StandardScaler — drop in if available
├── requirements.txt
├── README.md
├── templates/
│   └── index.html          # Single-page UI
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Quick Start

```bash
# 1. Clone / download the repo
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py
# → http://127.0.0.1:5000
```

## API Reference

### `POST /predict`

**Request body (JSON)**
```json
{
  "income":    52000,
  "age":       44,
  "recency":   20,
  "spending":  1200,
  "purchases": 18,
  "webvisits": 4
}
```

**Response (JSON)**
```json
{
  "cluster":     3,
  "name":        "VIP Customers",
  "emoji":       "👑",
  "color":       "#eab308",
  "description": "High-income, high-spending top-tier customers...",
  "tags":        ["High Income", "High Spending", "Top Tier"]
}
```

## Scaling Note

Input features are **z-score normalised** before prediction.

- If you have a `scaler.pkl` (a fitted `StandardScaler`), drop it in the project root — it will be loaded automatically.
- If no scaler is present, the app applies built-in default statistics derived from a typical marketing CRM dataset.  
  For best accuracy, train and save your own scaler on the original dataset:

  ```python
  from sklearn.preprocessing import StandardScaler
  import pickle

  scaler = StandardScaler()
  scaler.fit(X_train)          # X_train: DataFrame with the 6 features
  with open("scaler.pkl", "wb") as f:
      pickle.dump(scaler, f)
  ```

## Tech Stack

- **Backend**: Python 3.11+, Flask 3.1, scikit-learn, NumPy  
- **Frontend**: Vanilla HTML / CSS / JS (zero dependencies)  
- **Model**: K-Means (k=4), 6 features, pre-trained with scikit-learn

---

Built for rapid customer intelligence — extend with your own cluster labels and CRM data.
