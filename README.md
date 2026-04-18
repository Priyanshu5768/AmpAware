# AmpAware - AI-Powered Energy Intelligence
> AI-Powered Energy Intelligence for Indian Households - Predict electricity bills, detect anomalies, and calculate carbon footprint.

---

## 📌 Features

| Module | Description |
|--------|------------|
| 📊 **Dashboard** | Visual overview with monthly trends, pie charts, and AI insights |
| 🔌 **Appliance Manager** | Add household devices and see per-appliance breakdown |
| 🌱 **Carbon Impact** | Calculate CO₂ emissions and tree offset equivalents |
| 🔮 **AI Forecasting** | Predict future demand using weighted moving average |
| 🎮 **What-If Simulator** | Simulate savings from lifestyle changes |

---

## 🚀 Demo

### Running Locally

```bash
# Clone or download this repository
cd AmpAware

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.


## 🛠️ How It Works

### 1. Energy Consumption Calculation
```python
Units = (Watts × Hours × Days) / 1000
```

### 2. Carbon Footprint
```python
CO₂ = Units × 0.82 kg/kWh  # India grid emission factor
Trees = CO₂ / 20 kg per year
```

### 3. AI Forecasting
- **Weighted Moving Average**: Recent months get higher weight
- **Z-Score Anomaly Detection**: Flags unusual consumption spikes

---

## 📂 Project Structure

```
AmpAware/
├── app.py                    # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                # This file
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Programming language |
| Streamlit | Web application framework |
| Plotly | Interactive data visualizations |
| Pandas | Data manipulation |
| NumPy | Numerical computations |

---

## 🤖 AI/ML Techniques

1. **Weighted Moving Average** - For demand forecasting
2. **Z-Score Anomaly Detection** - For identifying unusual patterns

---

## 📥 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## ☁️ Deployment

Coming Soon....

---

## 🖼️ Screenshots

### Dashboard

<img width="905" height="503" alt="AmpAware Dashboard SS" src="https://github.com/user-attachments/assets/167933e8-3a4d-4148-b53a-567df53f087a" />


### Appliances

<img width="530" height="444" alt="AmpAware Appliances SS" src="https://github.com/user-attachments/assets/08624ab0-8793-496a-b006-6a0727f76cef" />


### Carbon Impact

<img width="892" height="498" alt="AmpAware Carbon SS" src="https://github.com/user-attachments/assets/9c9cad8e-d79a-4623-934a-afce7b65c67d" />


### AI Forecast

<img width="911" height="491" alt="AmpAware AI Forecast SS" src="https://github.com/user-attachments/assets/e38736b4-632b-4856-9b51-27812d265f10" />


### What-If Simulator

<img width="910" height="503" alt="AmpAware What If SS" src="https://github.com/user-attachments/assets/5f58a7c5-9c36-4c8d-aca2-901510e61734" />


## 📝 License

This is an educational **Mini Project** as a part of my B-Tech in Computer Science And Engineering.

---

## 👨‍🎓 Author

**Priyanshu Kumar**
- Roll No. 2401331690046
- B.Tech CSE (R) 2nd Year
- NIET (Noida Institute of Engineering and Technology),Greater Noida

---

## 🙏 Acknowledgments

- CO₂ emission factors from Ministry of Power, India
- Weighted Moving Average and Z-Score anomaly detection concepts 
  referenced from GeeksforGeeks and Towards Data Science.
- ML Concepts from CodewithHarry!

---
<p align="center">
  Made with ⚡ for a sustainable future
</p>
