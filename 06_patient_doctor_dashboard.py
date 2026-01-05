import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

@st.cache_data
def load_data():
    profiles = pd.read_csv('patient_profiles.csv')
    predictions = pd.read_csv('ncrs_predictions.csv')
    trajectories = pd.read_csv('trajectory_forecasts.csv')
    return profiles, predictions, trajectories

profiles, predictions, trajectories = load_data()
st.set_page_config(page_title="NCRS-AI", layout="wide")

# Patient Input Form 
st.markdown("### 👤 **New Patient Input**")
with st.expander("📝 Enter Patient Data for Real-Time Analysis", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=65)
        gender = st.selectbox("Gender", [0, 1], format_func=lambda x: "Male" if x==0 else "Female")
        disease_type = st.selectbox("Disease", [0, 1], format_func=lambda x: "Diabetes" if x==0 else "Hypertension")
    
    with col2:
        med_adherence = st.slider("Medication Adherence (Last 7 days %)", 0.0, 100.0, 50.0) / 100
        avg_activity = st.slider("Avg Daily Activity (minutes)", 0, 120, 20)
        bp = st.number_input("Latest BP (Systolic)", 90, 200, 170)
        glucose = st.number_input("Latest Glucose (mg/dL)", 70, 300, 220)
    
    if st.button("🔮 **Calculate NCRS Score**"):
        med_score = (1 - med_adherence) * 100
        activity_score = max(0, (60 - avg_activity) / 60 * 100)
        health_score = max(10, min(80, (abs(bp-130)/20 + abs(glucose-140)/40) * 30))
        diet_score = 25
        
        real_time_ncrs = round(0.35 * med_score + 0.20 * diet_score + 0.15 * activity_score + 0.30 * health_score, 1)
        
        st.success(f"**🩺 Real-Time NCRS: {real_time_ncrs}%**")
        risk_level = "🟢 Stable" if real_time_ncrs <= 30 else "🟡 Moderate" if real_time_ncrs <= 60 else "🔴 Critical"
        st.markdown(f"**Risk Level:** {risk_level}")
        
        if real_time_ncrs > 60:
            st.error(" **CRITICAL** - Contact doctor immediately!")
            st.markdown("**தமிழ்:** உடனடியாக மருத்துவரை அணுகவும்! ⚠️")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Age", age)
        with col2: st.metric("Activity", f"{avg_activity}min")
        with col3: st.metric("Health", f"BP:{bp} G:{int(glucose)}")

# Sidebar
view = st.sidebar.selectbox("Choose View:", ["👤 Patient Dashboard", "👨‍⚕️ Doctor Dashboard"])

if view == "👤 Patient Dashboard":
    st.title("🩺 NCRS-AI Patient Dashboard")
    
    patient_id = st.selectbox("Select Patient:", trajectories['patient_id'].unique())
    patient_data = trajectories[trajectories['patient_id'] == patient_id].iloc[0]
    
    # TWO METRICS: Current vs Predicted NCRS
    col1, col2 = st.columns(2)
    with col1:
        st.metric(" Current NCRS", f"{patient_data['predicted_ncrs']:.0f}%", 
                 delta=f"+{patient_data['risk_change']:.0f}")
    with col2:
        st.metric(" Predicted NCRS (Day 7)", f"{patient_data['day7_ncrs']:.0f}%", 
                 delta=f"{patient_data['day7_ncrs'] - patient_data['predicted_ncrs']:.0f}")
    
    # Risk level display
    risk_color = "🟢" if patient_data['predicted_ncrs'] <= 30 else "🟡" if patient_data['predicted_ncrs'] <= 60 else "🔴"
    st.markdown(f"**{risk_color} Current Risk Level:** {patient_data['predicted_risk_level']}")
    st.markdown(f" Trajectory: {patient_data['trajectory_risk']}")
    
    # Trajectory chart 
    with st.container():
        fig = go.Figure()
        days = [0, 1, 4, 7]
        ncrs_values = [patient_data['predicted_ncrs'], patient_data['day1_ncrs'], 
                      patient_data['day4_ncrs'], patient_data['day7_ncrs']]
        fig.add_trace(go.Scatter(x=days, y=ncrs_values, mode='lines+markers', 
                                name='NCRS Trend', line=dict(color='orange', width=3)))
        fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="CRITICAL")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="SAFE")
        fig.update_layout(title="Current → Predicted NCRS Trajectory", 
                         xaxis_title="Days", yaxis_title="NCRS %", height=400)
        st.plotly_chart(fig, width='stretch')


    st.subheader(" Adaptive Care Plan")
    ncrs = patient_data['predicted_ncrs']
    
    if ncrs > 60:
        st.error(" **CRITICAL** - Doctor consultation required!")
        st.success("**English:** Take ALL medications TODAY. Call doctor.")
        st.info("**தமிழ்:** இன்றே அனைத்து மருந்துகளையும் எடுத்துக்கொள்ளுங்கள். மருத்துவரை அழைக்கவும்!")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(" Medication:  Take ALL doses TODAY. Call doctor.")
        with col2: st.markdown(" Diet: Strict low-carb diet. No sweets.")
        with col3: st.markdown(" Activity: 30min walk TODAY. Emergency.")
        
    elif ncrs > 30:
        st.warning("⚠️ **HIGH RISK** - Extra caution needed!")
        st.success("**English:** Double-check ALL medications this week.")
        st.info("**தமிழ்:** இந்த வாரம் அனைத்து மருந்துகளையும் இரட்டிப்பு சரிபார்க்கவும்!")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(" Medication: Double-check ALL doses.")
        with col2: st.markdown(" Diet: Reduce salt/sugar by 50%.")
        with col3: st.markdown(" Activity: 45min daily walk M-F.")
        
    else:
        st.success(" **STABLE** - Excellent compliance!")
        st.success("**English:** Great job! Keep it up!")
        st.info("**தமிழ்:** சிறப்பாக செய்கிறீர்கள்! தொடருங்கள்! 👍")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(" Medication: Continue current doses.")
        with col2: st.markdown(" Diet: Maintain healthy diet.")
        with col3: st.markdown(" Activity: 30min daily walk.")

elif view == "👨‍⚕️ Doctor Dashboard":
    st.title(" NCRS-AI Doctor Dashboard")
    
    risk_filter = st.selectbox("Filter by Risk:", ["All", "Fragile", "Moderate", "Stable"])
    df_display = trajectories.copy()
    
    if risk_filter != "All":
        df_display = df_display[df_display['predicted_risk_level'] == risk_filter]
    
    st.subheader(" Top 10 Highest Risk Patients")
    top_risk = df_display.nlargest(10, 'day7_ncrs')[[
        'patient_id', 'predicted_ncrs', 'day7_ncrs', 'risk_change',
        'trajectory_risk', 'predicted_risk_level'
    ]].round(1)
    st.dataframe(top_risk, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(df_display, names='predicted_risk_level', title="Risk Distribution")
        st.plotly_chart(fig_pie, width='stretch')
    
    with col2:
        critical = df_display[df_display['trajectory_risk'] == 'Critical Trajectory']
        if not critical.empty:
            fig_bar = px.bar(critical.head(10), x='patient_id', y='day7_ncrs', 
                           title="Critical Trajectory Patients")
            st.plotly_chart(fig_bar, width='stretch')
    
    st.download_button(" Download Full Report", 
                      trajectories.to_csv(index=False), 
                      "ncrs_report.csv", "text/csv")

st.markdown("---")
st.markdown("*NCRS-AI: Non-Compliance Risk Scoring for Chronic Disease Care*")
