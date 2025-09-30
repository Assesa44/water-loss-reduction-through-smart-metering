import streamlit as st
import joblib
import pandas as pd
from io import BytesIO
import os

# Define correct model path (relative to app.py in root folder)
MODEL_PATH = os.path.join("Notebooks", "Exploratory", "kmeans_model.pkl")

# =========================
# Cache Model Loading
# =========================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f" Failed to load model from {MODEL_PATH}. Error: {e}")
    st.stop()

# Streamlit App Title
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
    cluster = int(prediction[0])  # ensure integer for indexing
    input_data["Cluster"] = cluster
    input_data["Insights"] = cluster_insights.get(cluster, "No insight available")

    st.success(f"🔎 This customer belongs to **Cluster {cluster}**")

    # Show additional info
    st.dataframe(input_data)

    if cluster == 0:
        st.warning("💡 Recommendation: Focus on leak detection in residential areas.")
    elif cluster == 1:
        st.warning("💡 Recommendation: Monitor billing compliance for SMEs.")
    elif cluster == 2:
        st.warning("💡 Recommendation: Prioritize smart metering rollout in commercial/industrial zones.")

    # Enable CSV download for single prediction
    output_single = BytesIO()
    input_data.to_csv(output_single, index=False)
    output_single.seek(0)

    st.download_button(
        label="⬇️ Download Single Prediction as CSV",
        data=output_single,
        file_name="single_prediction.csv",
        mime="text/csv"
    )

# =========================
# CSV Upload & Batch Prediction
# =========================
st.subheader("📂 Upload CSV for Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file with BILL_VOLUME, BILL_AMOUNT, and METER_SIZE columns", 
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write(" Uploaded Data Preview:")
    st.dataframe(data.head())

    try:
        predictions = model.predict(data[["BILL_VOLUME", "BILL_AMOUNT", "METER_SIZE"]])
        data["Cluster"] = predictions
        data["Insights"] = data["Cluster"].map(cluster_insights)

        st.success("✅ Clusters assigned successfully!")
        st.dataframe(data.head())

        # Download results
        output = BytesIO()
        data.to_csv(output, index=False)
        output.seek(0)

        st.download_button(
            label="⬇ Download Batch Results as CSV",
            data=output,
            file_name="clustered_results.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f" Error during batch prediction: {e}")
