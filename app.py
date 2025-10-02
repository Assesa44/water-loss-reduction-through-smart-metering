import streamlit as st
import joblib
import pandas as pd
from io import BytesIO
import os
from PIL import Image


logo = Image.open("logo.png")

MODEL_PATH = os.path.join("Notebooks", "Exploratory", "kmeans_model.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f" Failed to load model from {MODEL_PATH}. Error: {e}")
    st.stop()


st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(logo, width=150)  # slightly bigger logo
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center; margin-top: -10px;'>💧 Water Loss Reduction - Smart Metering Clustering</h1>",
    unsafe_allow_html=True
)


st.markdown("## 📌 Project Description")
st.info(
    "This app applies **KMeans clustering** to group water consumers "
    "based on meter size, bill volume, and bill amount. "
    "It helps utilities identify customers for smart metering rollout."
)


st.markdown("## 🔹 Model Clusters")
st.success("""  
- **Cluster 0**: Low usage, small meters, minimal billing — Residential.  
- **Cluster 1**: Medium usage, varied meters, moderate bills — SMEs.  
- **Cluster 2**: High usage, large meters, high bills — Industrial/Commercial.  
""")

st.write("You can either enter details manually or upload a CSV file for batch clustering.")
cluster_insights = {
    0: "Cluster 0: Low usage, small meters, minimal billing — likely residential customers.",
    1: "Cluster 1: Medium usage, varied meter sizes, moderate bills — could be small businesses.",
    2: "Cluster 2: High usage, large meters, high bills — likely commercial/industrial customers.",
}


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
    cluster = int(prediction[0])
    input_data["Cluster"] = cluster
    input_data["Insights"] = cluster_insights.get(cluster, "No insight available")

    st.success(f"🔎 This customer belongs to **Cluster {cluster}**")
    st.table(input_data)

    if cluster == 0:
        st.warning(" Recommendation: Focus on leak detection in residential areas.")
    elif cluster == 1:
        st.warning(" Recommendation: Monitor billing compliance for SMEs.")
    elif cluster == 2:
        st.warning(" Recommendation: Prioritize smart metering rollout in commercial/industrial zones.")

    # Enable CSV download for single prediction
    output_single = BytesIO()
    input_data.to_csv(output_single, index=False)
    output_single.seek(0)

    st.download_button(
        label="⬇ Download Single Prediction as CSV",
        data=output_single,
        file_name="single_prediction.csv",
        mime="text/csv"
    )


st.subheader("📂 Upload CSV for Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file with BILL_VOLUME, BILL_AMOUNT, and METER_SIZE columns",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("📊 Uploaded Data Preview:")
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
            label="⬇️ Download Batch Results as CSV",
            data=output,
            file_name="clustered_results.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"❌ Error during batch prediction: {e}")


st.markdown("---")
st.markdown("### 📬 Contact")
st.write("Developed by **Group3**")
st.write("✉️ Email: veesandra30@gmail.com")
st.write("[🌐 GitHub](https://github.com/Assesa44/water-loss-reduction-through-smart-metering.git)")
