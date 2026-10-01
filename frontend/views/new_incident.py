import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_new_incident():
    st.title("➕ Create & Analyze New Incident")
    st.write("Submit an operational issue for instant database logging and automated classification.")

    with st.form("new_incident_form"):
        title = st.text_input("Incident Title *", "Cannot connect to Cisco AnyConnect VPN")
        description = st.text_area("Detailed Description *", "User receives network connection timeout error when connecting to Mumbai VPN gateway.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
        with col2:
            affected_users = st.number_input("Affected Users", min_value=1, max_value=10000, value=25)
        with col3:
            criticality = st.selectbox("System Criticality", ["Low", "Medium", "High", "Critical"])

        submit = st.form_submit_button("Log & Analyze Incident", type="primary")

    if submit:
        if len(title) < 5 or len(description) < 10:
            st.error("Title must be at least 5 chars and Description at least 10 chars.")
            return

        with st.spinner("Saving ticket and executing AI analysis pipeline..."):
            payload = {
                "title": title,
                "description": description,
                "category": category,
                "system_criticality": criticality,
                "affected_users": affected_users
            }
            try:
                # Log incident to backend database
                res_inc = requests.post(f"{BACKEND_URL}/incidents", json={"title": title, "description": description, "category": category, "priority": "Pending"})
                
                # Execute full AI analysis
                res_ai = requests.post(f"{BACKEND_URL}/analysis/resolve", json=payload)
                
                if res_ai.status_code == 200:
                    data = res_ai.json()
                    st.success("✅ Incident logged and analyzed successfully!")
                    
                    st.markdown("---")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Predicted Priority", data["predicted_priority"])
                    m2.metric("ML Confidence", f"{int(data['ml_confidence']*100)}%")
                    m3.metric("Escalation Needed", "YES" if data["escalation_needed"] else "NO")

                    st.subheader("📋 Recommended Actions")
                    for step in data["recommended_steps"]:
                        st.write(f"- {step}")
                else:
                    st.error("AI Analysis failed.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")