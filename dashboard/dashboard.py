import streamlit as st
import pandas as pd
from rag_pipeline_runner import query_rag_llm

st.set_page_config(
    page_title="AI Security Analyst",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .report-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI RAG Security Threat Prioritizer")
st.markdown("### Real-time Threat Analysis Dashboard")

# --- Sidebar: Configuration & Filtering ---
st.sidebar.header("Configuration")
st.sidebar.info("Ensure `OPENAI_API_KEY` is set in your environment.")

st.sidebar.header("Filter Alerts")
severity_filter = st.sidebar.multiselect(
    "Select Severity Levels",
    options=["Critical", "High", "Medium", "Low"],
    default=["Critical", "High"]
)

# --- Mock Data: Incoming Alerts ---
# In a real app, this would come from a SIEM or database
alerts_data = [
    {
        "id": 101,
        "type": "Suspicious Login Attempt",
        "severity": "High",
        "score": 0.89,
        "timestamp": "2025-12-26 10:45:00",
        "description": "User 'admin' had 15 failed login attempts followed by a successful one provided by a known malicious IP."
    },
    {
        "id": 102,
        "type": "Potential SQL Injection",
        "severity": "Critical",
        "score": 0.95,
        "timestamp": "2025-12-26 11:12:30",
        "description": "Detected URL payload containing 'OR 1=1' logic in login endpoint requests."
    },
    {
        "id": 103,
        "type": "Unusual Data Egress",
        "severity": "Medium",
        "score": 0.65,
        "timestamp": "2025-12-26 11:30:15",
        "description": "Outbound traffic to unrecognized IP address exceeded 500MB in 10 minutes."
    }
]

# --- Main Dashboard Logic ---

# Filter data based on sidebar selection
filtered_alerts = [alert for alert in alerts_data if alert["severity"] in severity_filter]

# Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Alerts", len(alerts_data))
col2.metric("Visible Alerts", len(filtered_alerts))
col3.metric("Critical Threats", len([a for a in alerts_data if a["severity"] == "Critical"]))

st.divider()

if not filtered_alerts:
    st.success("✅ No alerts match your filter criteria.")
else:
    for alert in filtered_alerts:
        # Create an expander for each alert
        with st.expander(f"{alert['severity']} | {alert['type']} (Score: {alert['score']})", expanded=False):
            
            # Layout: Details on left, Actions on right
            d_col1, d_col2 = st.columns([3, 1])
            
            with d_col1:
                st.markdown(f"**Timestamp:** {alert['timestamp']}")
                st.markdown(f"**Description:** {alert['description']}")
                
            with d_col2:
                analyze_btn = st.button(f"🔍 Analyze Alert #{alert['id']}", key=f"btn_{alert['id']}")
            
            # If button clicked, run the RAG pipeline
            if analyze_btn:
                with st.spinner("🤖 AI Analyst is investigating context and policies..."):
                    # Call the function from rag_pipeline_runner.py
                    analysis_result = query_rag_llm(
                        alert_type=alert["type"],
                        severity=alert["severity"],
                        anomaly_score=str(alert["score"]),
                        description=alert["description"]
                    )
                
                # Display Result
                st.markdown("### 📝 AI Threat Report")
                st.markdown(analysis_result)
