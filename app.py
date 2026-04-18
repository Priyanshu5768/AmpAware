import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AmpAware - AI-Powered Energy Intelligence", page_icon="⚡", layout="wide")

EMISSION_FACTOR = 0.82
TREE_ABSORPTION = 20

INDIAN_TARIFF = {
    'delhi': [(0, 200, 3.0), (200, 400, 4.5), (400, 1000, 6.0)],
    'mumbai': [(0, 100, 3.3), (100, 200, 4.7), (200, 300, 5.6), (300, 400, 6.8), (400, 1000, 7.5)],
    'bangalore': [(0, 200, 4.5), (200, 400, 5.8), (400, 1000, 6.9)],
    'kolkata': [(0, 200, 4.2), (200, 400, 5.4), (400, 1000, 6.5)],
    'chennai': [(0, 100, 2.5), (100, 200, 3.5), (200, 300, 4.5), (300, 400, 5.8), (400, 1000, 6.7)],
}

APPLIANCE_DATABASE = {
    'AC': {'watts': 1500, 'type': 'peak'},
    'Refrigerator': {'watts': 150, 'type': 'base'},
    'Geyser': {'watts': 2000, 'type': 'peak'},
    'Washing Machine': {'watts': 500, 'type': 'variable'},
    'LED TV': {'watts': 100, 'type': 'variable'},
    'Ceiling Fan': {'watts': 75, 'type': 'base'},
    'Microwave': {'watts': 1200, 'type': 'variable'},
    'Iron': {'watts': 1000, 'type': 'variable'},
    'Water Pump': {'watts': 750, 'type': 'peak'},
    'Computer/Laptop': {'watts': 150, 'type': 'variable'},
    'Lights': {'watts': 60, 'type': 'base'},
    'Router': {'watts': 10, 'type': 'base'},
    'WiFi Box': {'watts': 15, 'type': 'base'},
    'Dishwasher': {'watts': 1200, 'type': 'variable'},
    'Electric Kettle': {'watts': 1500, 'type': 'variable'},
    'Oven': {'watts': 2000, 'type': 'variable'},
    'Air Cooler': {'watts': 200, 'type': 'peak'},
    'Heater': {'watts': 1500, 'type': 'peak'},
}

def calculate_units(watts, hours, days):
    return (watts * hours * days) / 1000

def calculate_bill(units, city):
    slab = INDIAN_TARIFF[city]
    total = 0
    remaining = units
    for i, (lower, upper, rate) in enumerate(slab):
        if remaining <= 0:
            break
        if i == len(slab) - 1:
            total += remaining * rate
            break
        slab_units = min(remaining, upper - lower)
        total += slab_units * rate
        remaining -= slab_units
    return round(total, 2)

def calculate_carbon(units):
    return round(units * EMISSION_FACTOR, 2)

def trees_equivalent(kg_co2):
    return round(kg_co2 / TREE_ABSORPTION, 1)

def predict_future(historical_units, days_to_predict=30):
    if len(historical_units) < 2:
        return historical_units[-1] if historical_units else 0
    n = len(historical_units)
    weights = np.arange(1, n + 1)
    weighted_avg = np.average(historical_units, weights=weights)
    trend = (historical_units[-1] - historical_units[0]) / n if n > 1 else 0
    return round(weighted_avg + trend * (days_to_predict / 30), 2)

def detect_anomaly(current, historical):
    if len(historical) < 3:
        return None, 0
    avg = np.mean(historical)
    std = np.std(historical)
    if std == 0:
        return None, 0
    z_score = (current - avg) / std
    if z_score > 1.5:
        return "HIGH", z_score
    elif z_score < -1.5:
        return "LOW", z_score
    return "NORMAL", z_score

def style():
    st.markdown("""
    <style>
    .main { background: #0a0a0a; }
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); }
    h1, h2, h3 { color: #00d4ff !important; font-weight: 700; }
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #252545);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00d4ff33;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
    }
    .highlight { color: #00ffcc; font-weight: bold; }
    .warning { color: #ff6b6b; font-weight: bold; }
    .success { color: #00ff88; font-weight: bold; }
    div.stButton > button {
        background: linear-gradient(90deg, #00d4ff, #00ffcc);
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        color: #000;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def sidebar():
    st.sidebar.markdown("## ⚡ AmpAware")
    st.sidebar.markdown("*AI-Powered Energy Intelligence*")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Navigation", 
        ["🏠 Dashboard", "🔌 Appliances", "🌱 Carbon Impact", 
         "🔮 AI Forecast", "🎮 What-If Simulator"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Quick Stats")
    st.sidebar.metric("Energy Saved", "24%", delta="-₹1,200")
    st.sidebar.metric("Carbon Reduced", "480 kg", delta="-10%")
    
    return menu

def dashboard():
    st.markdown("# ⚡ AmpAware Dashboard")
    st.markdown("*AI-Powered Energy Intelligence for Indian Households*")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚡ Total Units", "485 kWh", "↑ 12%")
    with col2:
        st.metric("💰 Est. Bill", "₹4,850", "↑ ₹450")
    with col3:
        st.metric("🌍 CO₂ Emissions", "398 kg", "↑ 12%")
    with col4:
        st.metric("🌳 Trees Needed", "20 trees", "↑ 2")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Monthly Consumption Trend")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        units_data = [280, 295, 340, 420, 485, 520]
        fig = px.bar(x=months, y=units_data, labels={'x': 'Month', 'y': 'Units (kWh)'},
                   color=units_data, color_continuous_scale='Viridis')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🍰 Consumption Breakdown")
        labels = ['AC', 'Refrigerator', 'Lighting', 'Others']
        values = [35, 22, 18, 25]
        fig = px.pie(values=values, names=labels, hole=0.5,
                   color_discrete_sequence=['#00d4ff', '#00ffcc', '#ff6b6b', '#ffd93d'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔔 AI Insights")
        st.info("🔍 **Anomaly Detected:** Base load increased by 15% over last 3 months. Check refrigerator efficiency.")
        st.success("💡 **Tip:** Reducing AC by 1 hour/day can save ₹850/month!")
    
    with col2:
        st.markdown("### 📉 Weekly Usage Pattern")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        usage = [18, 19, 17, 20, 18, 22, 21]
        fig = px.line(x=days, y=usage, markers=True, 
                    labels={'x': 'Day', 'y': 'Units'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white')
        st.plotly_chart(fig, use_container_width=True)

def appliances():
    st.markdown("# 🔌 Appliance Manager")
    st.markdown("*Add and manage your household appliances*")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ➕ Add Appliance")
        
        with st.form("add_appliance"):
            appliance_name = st.selectbox("Select Appliance", 
                list(APPLIANCE_DATABASE.keys()) + ["Custom"])
            
            if appliance_name == "Custom":
                name = st.text_input("Appliance Name")
                watts = st.number_input("Power (Watts)", 10, 5000, 100)
            else:
                name = appliance_name
                watts = APPLIANCE_DATABASE[appliance_name]['watts']
                st.metric("Power Rating", f"{watts}W")
            
            quantity = st.number_input("Quantity", 1, 20, 1)
            hours = st.slider("Hours/Day", 0.0, 24.0, 2.0, 0.5)
            
            submitted = st.form_submit_button("➕ Add Appliance")
            
            if submitted:
                st.session_state.setdefault('appliances', []).append({
                    'name': name, 'watts': watts, 'quantity': quantity,
                    'hours': hours, 'days': 30
                })
                st.success(f"Added {name}!")
    
    if 'appliances' in st.session_state and st.session_state.appliances:
        st.markdown("### 📋 Your Appliances")
        
        for i, app in enumerate(st.session_state.appliances):
            units = calculate_units(app['watts'] * app['quantity'], app['hours'], app['days'])
            st.session_state.appliances[i]['units'] = units
        
        df = pd.DataFrame(st.session_state.appliances)
        df['Cost'] = df['units'].apply(lambda x: calculate_bill(x, 'delhi'))
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df[['name', 'watts', 'quantity', 'hours', 'units']], use_container_width=True)
        with col2:
            total_units = df['units'].sum()
            total_cost = df['Cost'].sum()
            total_carbon = calculate_carbon(total_units)
            
            st.metric("Total Units", f"{total_units:.1f} kWh")
            st.metric("Estimated Bill", f"₹{total_cost:.2f}")
            st.metric("CO₂ Emissions", f"{total_carbon:.1f} kg")
        
        if st.button("🗑️ Clear All"):
            st.session_state.appliances = []
            st.rerun()
    else:
        st.info("No appliances added yet. Add your first appliance above!")

def carbon_impact():
    st.markdown("# 🌱 Carbon Impact Analyzer")
    st.markdown("*Understand your environmental footprint*")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        units = st.number_input("Monthly Units (kWh)", 0, 2000, 485)
        days = st.slider("Period (Days)", 1, 365, 30)
    
    with col2:
        carbon_per_month = calculate_carbon(units)
        carbon_per_year = carbon_per_month * 12
        trees_needed = trees_equivalent(carbon_per_year)
        
        st.metric("Monthly CO₂", f"{carbon_per_month} kg")
        st.metric("Yearly CO₂", f"{carbon_per_year} kg")
        st.metric("🌳 Trees to Offset", f"{trees_needed} trees")
    
    if units > 0:
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Carbon Footprint Breakdown")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            seasonal_factor = [0.7, 0.7, 0.8, 1.0, 1.3, 1.5, 1.6, 1.5, 1.2, 0.9, 0.8, 0.7]
            monthly_carbon = [carbon_per_month * f for f in seasonal_factor]
            
            fig = px.bar(x=months, y=monthly_carbon, labels={'x': 'Month', 'y': 'CO₂ (kg)'},
                       color=monthly_carbon, color_continuous_scale='Greens')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Reduction Impact")
            
            reduction_10 = carbon_per_year * 0.1
            reduction_20 = carbon_per_year * 0.2
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Reduce 10%", f"-{reduction_10:.0f} kg CO₂", 
                         delta=f"-{trees_equivalent(reduction_10):.1f} trees")
            with col_b:
                st.metric("Reduce 20%", f"-{reduction_20:.0f} kg CO₂",
                         delta=f"-{trees_equivalent(reduction_20):.1f} trees")
        
        st.markdown("### 🌳 Environmental Impact Visualization")
        
        chart_data = pd.DataFrame({
            'Category': ['Your CO₂', 'Car (100km/month)', 'Flight (Delhi-Mumbai)', 'Average Indian'],
            'kg CO₂/year': [carbon_per_year, 2400, 320, 1200]
        })
        
        fig = px.bar(chart_data, x='Category', y='kg CO₂/year', 
                    color='kg CO₂/year', color_continuous_scale='Reds')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white')
        st.plotly_chart(fig, use_container_width=True)

def ai_forecast():
    st.markdown("# 🔮 AI Demand Forecasting")
    st.markdown("*Predict future electricity consumption using ML*")
    st.markdown("---")
    
    st.markdown("### 📈 Enter Historical Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_months = st.slider("Number of months", 2, 12, 6)
    
    units_history = []
    for i in range(num_months):
        val = st.number_input(f"Month {i+1} units", 0, 2000, 280 + i*40)
        units_history.append(val)
    
    if len(units_history) >= 2:
        predicted = predict_future(units_history, 30)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_units = np.mean(units_history)
            st.metric("📊 Average Usage", f"{avg_units:.1f} kWh")
        
        with col2:
            trend = (units_history[-1] - units_history[0]) / len(units_history)
            trend_str = "↑" if trend > 0 else "↓"
            st.metric(f"{trend_str} Trend", f"{abs(trend):.1f}/month", 
                    delta=trend_str)
        
        with col3:
            predicted_bill = calculate_bill(predicted, 'delhi')
            conf = min(87, 50 + len(units_history) * 5)
            st.metric("🔮 Prediction", f"₹{predicted_bill}", 
                    delta=f"{conf}% confidence")
        
        st.markdown("### 📈 Forecast Visualization")
        
        months = [f"Month {i+1}" for i in range(len(units_history))] + ["Next Month"]
        all_units = units_history + [predicted]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months[:-1], y=units_history, 
                              mode='lines+markers', name='Historical',
                              line=dict(color='#00d4ff', width=3)))
        fig.add_trace(go.Scatter(x=[months[-1]], y=[predicted],
                              mode='markers', name='Predicted',
                              marker=dict(color='#ff6b6b', size=15)))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='white', xaxis_title='Month', yaxis_title='Units')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🔍 Anomaly Detection")
        
        if len(units_history) >= 3:
            status, z = detect_anomaly(units_history[-1], units_history[:-1])
            
            if status == "HIGH":
                st.warning(f"⚠️ Anomaly Detected! Usage is {z:.1f}σ above average. Investigate!")
            elif status == "LOW":
                st.success(f"✅ Usage is {abs(z):.1f}σ below average. Great efficiency!")
            else:
                st.info("✅ No anomalies detected. Usage is within normal range.")
        
        st.markdown("### 📋 Seasonal Pattern Analysis")
        
        seasons = {
            'Summer (Mar-Jun)': np.mean(units_history[2:5]) if len(units_history) >= 5 else units_history[-1],
            'Monsoon (Jul-Oct)': np.mean(units_history[4:8]) if len(units_history) >= 8 else units_history[-1],
            'Winter (Nov-Feb)': np.mean(units_history[:2]) if len(units_history) >= 2 else units_history[-1]
        }
        
        fig = px.bar(x=list(seasons.keys()), y=list(seasons.values()),
                   labels={'x': 'Season', 'y': 'Average Units'},
                   color=list(seasons.values()), color_continuous_scale='Viridis')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='white')
        st.plotly_chart(fig, use_container_width=True)

def whatif_simulator():
    st.markdown("# 🎮 What-If Simulator")
    st.markdown("*Simulate scenarios and see potential savings*")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        base_units = st.number_input("Base Monthly Units", 0, 2000, 485)
    
    with col2:
        city = st.selectbox("City", list(INDIAN_TARIFF.keys()))
    
    st.markdown("### 🎯 Select Simulation Scenarios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ac_reduction = st.slider("Reduce AC Usage (hrs/day)", 0, 8, 0)
        ac_savings = 0
        if ac_reduction > 0:
            ac_savings = (1500 * ac_reduction * 30 / 1000)
            units_saved = ac_savings
            money_saved = calculate_bill(min(base_units, units_saved), city) if base_units >= units_saved else 0
            st.success(f"💰 Save ₹{calculate_bill(ac_savings, city):.0f}/month")
        else:
            units_saved = 0
            st.caption("No change")
    
    with col2:
        fridge_upgrade = st.checkbox("Upgrade to 5-Star Fridge")
        if fridge_upgrade and base_units > 0:
            fridge_savings = 50
            st.success(f"💰 Save ₹{calculate_bill(fridge_savings, city):.0f}/month")
            units_saved += fridge_savings
        else:
            fridge_savings = 0
    
    with col3:
        led_switch = st.checkbox("Switch to LED Lights")
        if led_switch and base_units > 0:
            led_savings = 30
            st.success(f"💰 Save ₹{calculate_bill(led_savings, city):.0f}/month")
            units_saved += led_savings
        else:
            led_savings = 0
    
    total_savings = ac_savings + fridge_savings + led_savings
    
    if total_savings > 0:
        st.markdown("---")
        
        monthly_savings_money = calculate_bill(total_savings, city)
        yearly_savings = monthly_savings_money * 12
        carbon_reduced = calculate_carbon(total_savings)
        yearly_carbon_reduced = carbon_reduced * 12
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Monthly Savings", f"₹{monthly_savings_money:.0f}")
        with col2:
            st.metric("💰 Yearly Savings", f"₹{yearly_savings:.0f}")
        with col3:
            st.metric("🌍 Carbon Reduced", f"{carbon_reduced:.1f} kg/month")
        with col4:
            st.metric("🌳 Yearly Offset", f"{trees_equivalent(yearly_carbon_reduced):.1f} trees")
        
        st.markdown("### 📊 Savings Breakdown")
        
        before_bill = calculate_bill(base_units, city)
        after_bill = calculate_bill(base_units - total_savings, city)
        
        comp_data = pd.DataFrame({
            'Scenario': ['Before', 'After'],
            'Bill (₹)': [before_bill, after_bill],
            'CO₂ (kg)': [calculate_carbon(base_units), calculate_carbon(base_units - total_savings)]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(comp_data, x='Scenario', y='Bill (₹)', 
                       color='Bill (₹)', color_continuous_scale='Greens')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(comp_data, x='Scenario', y='CO₂ (kg)',
                       color='CO₂ (kg)', color_continuous_scale='Oranges')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📅 6-Month Projection")
        
        months = list(range(1, 7))
        cumulative = [monthly_savings_money * m for m in months]
        
        fig = px.line(x=months, y=cumulative, markers=True,
                    labels={'x': 'Month', 'y': 'Cumulative Savings (₹)'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one scenario to see savings!")

def main():
    style()
    menu = sidebar()
    
    if menu == "🏠 Dashboard":
        dashboard()
    elif menu == "🔌 Appliances":
        appliances()
    elif menu == "🌱 Carbon Impact":
        carbon_impact()
    elif menu == "🔮 AI Forecast":
        ai_forecast()
    elif menu == "🎮 What-If Simulator":
        whatif_simulator()

if __name__ == "__main__":
    main()