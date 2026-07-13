# 📊 Sales Data Analytics Dashboard

An interactive Streamlit dashboard for analyzing **sales trends, profitability, top-selling products, and regional performance** — built as an internship project.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **KPI cards**: Total Sales, Total Profit, Total Orders, Avg Order Value, Profit Margin
- **Monthly sales & profit trend** line chart
- **Sales by category** breakdown (donut chart)
- **Top 10 products** by sales (with profit color-coding)
- **Regional performance** comparison (sales vs. profit)
- **Profit margin by category**
- **Sales by customer segment**
- **Interactive filters**: date range, region, category, customer segment
- **Raw data explorer** with CSV export of filtered results

---

## 🗂️ Project Structure

```
sales-dashboard/
├── app.py                 # Main Streamlit dashboard app
├── generate_data.py        # Script that generates the sample dataset
├── data/
│   └── sales_data.csv      # Sample sales dataset (~5,500 orders, 2024–2025)
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/sales-dashboard.git
   cd sales-dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`.

> Want to regenerate the sample data with different randomness? Run `python generate_data.py`.

---

## 📤 Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Sales Data Analytics Dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/sales-dashboard.git
git push -u origin main
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this project to a **public GitHub repository** (steps above).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **"New app"**.
4. Select your repository, the `main` branch, and set the main file path to `app.py`.
5. Click **"Deploy"**. Streamlit Cloud will install `requirements.txt` automatically and launch your app.
6. Your dashboard will be live at a URL like:
   `https://<your-username>-sales-dashboard.streamlit.app`

---

## 🔄 Using Your Own Data

Replace `data/sales_data.csv` with your own dataset, keeping (or remapping in `app.py`) these columns:

| Column | Type | Description |
|---|---|---|
| `Order_ID` | string | Unique order identifier |
| `Order_Date` | date | Order date (`YYYY-MM-DD`) |
| `Region` | string | Sales region |
| `Category` | string | Product category |
| `Product` | string | Product name |
| `Customer_Segment` | string | Consumer / Corporate / Small Business |
| `Ship_Mode` | string | Shipping method |
| `Quantity` | int | Units sold |
| `Discount` | float | Discount rate (0–1) |
| `Sales` | float | Revenue for the line item |
| `Profit` | float | Profit for the line item |

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — dashboard framework
- [Pandas](https://pandas.pydata.org/) — data processing
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
