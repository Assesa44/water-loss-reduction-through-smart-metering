import streamlit as st
import joblib
import pandas as pd
from io import BytesIO

# Load your trained model
model = joblib.load("kmeans_model.pkl")  

st.title("💧 Water Loss Reduction - Smart Metering Clustering")

st.write("You can either enter details manually or upload a CSV file for bulk clustering.")

# Predefined insights per cluster
cluster_insights = {
    0: "Cluster 0: Low usage, small meters, minimal billing — likely residential customers.",
    1: "Cluster 1: Medium usage, varied meter sizes, moderate bills — could be small businesses.",
    2: "Cluster 2: High usage, large meters, high bills — likely commercial/industrial customers.",
}

# =========================
# Manual Input
# =========================
st.subheader("🔹 Single Customer Prediction")

bill_volume = st.number_input("Bill Volume", min_value=0.0, step=0.1)
bill_amount = st.number_input("Bill Amount", min_value=0.0, step=0.1)
meter_size_value = st.number_input("Meter Size", min_value=0, step=1)

if st.button("Predict Cluster (Single)"):
    input_data = pd.DataFrame([{
        "BILL_VOLUME": bill_volume,
        "BILL_AMOUNT": bill_amount,
        "METER_SIZE": meter_size_value
    }])

    prediction = model.predict(input_data)
    cluster = prediction[0]

    st.success(f"🔎 This customer belongs to **Cluster {cluster}**")

    if cluster in cluster_insights:
        st.info(cluster_insights[cluster])

    if cluster == 0:
        st.warning("💡 Recommendation: Focus on leak detection in residential areas.")
    elif cluster == 1:
        st.warning("💡 Recommendation: Monitor billing compliance for SMEs.")
    elif cluster == 2:
        st.warning("💡 Recommendation: Prioritize smart metering rollout in commercial/industrial zones.")


# =========================
# CSV Upload & Batch Prediction
# =========================
st.subheader("📂 Upload CSV for Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file with BILL_VOLUME, BILL_AMOUNT, and METER_SIZE columns", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("📊 Uploaded Data Preview:")
    st.dataframe(data.head())

    # Predict clusters
    predictions = model.predict(data[["BILL_VOLUME", "BILL_AMOUNT", "METER_SIZE"]])
    data["Cluster"] = predictions
    data["Insights"] = data["Cluster"].map(cluster_insights)

    st.success("✅ Clusters assigned successfully!")
    st.dataframe(data.head())

    # Download button
    output = BytesIO()
    data.to_csv(output, index=False)
    output.seek(0)

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=output,
        file_name="clustered_results.csv",
        mime="text/csv"
    )
