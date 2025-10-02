import streamlit as st
import joblib
import pandas as pd
from io import BytesIO
import os
from PIL import Image
import matplotlib.pyplot as plt


logo = Image.open("logo.png")

# Model Path
MODEL_PATH = os.path.join("Notebooks", "Exploratory", "gmm_pipeline.joblib")

@st.cache_resource
def load_pipeline():
    return joblib.load(MODEL_PATH)

try:
    pipeline = load_pipeline()
except Exception as e:
    st.error(f" Failed to load model from {MODEL_PATH}. Error: {e}")
    st.stop()


st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(logo, width=150)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center; margin-top: -10px;'> Water Loss Reduction - Smart Metering Clustering</h1>",
    unsafe_allow_html=True
)

st.markdown("##  Description")
st.info(
    "This app applies a **Gaussian Mixture Model (GMM)** to segment water consumers into distinct behavioral clusters. "
    "Unlike simple clustering, GMM captures overlaps and variability in consumption, revealing more nuanced usage groups. "
    "By analyzing **water amount, sewer amount, bill amount, and bill volume**, the model helps utilities detect household, "
    "industrial, and potentially problematic users, supporting smarter metering and water loss reduction strategies."
)


st.write("👉 You can either enter details manually or upload a CSV file for batch clustering.")



cluster_insights = {
    0: "Cluster 0: Low-use Households → Small water & sewer usage, very stable billing. Mostly residential users with predictable, low demand.",
    1: "Cluster 1: SMEs/Moderate Commercial → Balanced and moderate water & sewer usage, slightly higher bills. Represents small-to-medium businesses.",
    2: "Cluster 2: Farms / NRW Risks → Water usage with very low sewer return. Suggests agriculture, irrigation, or possible non-revenue water (illegal connections/leaks).",
    3: "Cluster 3: Heavy Industry / High-demand Users → Highest water consumption, large bills, and heavy volumes. Represents industrial users or very large farms; requires close monitoring."
}




st.subheader("🔹 Single Customer Prediction")

water_amount = st.number_input("Water Amount", min_value=0.0, step=0.1)
sewer_amount = st.number_input("Sewer Amount", min_value=0.0, step=0.1)
bill_amount = st.number_input("Bill Amount", min_value=0.0, step=0.1)
bill_volume = st.number_input("Bill Volume", min_value=0.0, step=0.1)

if st.button("Predict Cluster (Single)"):
    input_data = pd.DataFrame([{
        "WATER_AMOUNT": water_amount,
        "SEWER_AMOUNT": sewer_amount,
        "BILL_AMOUNT": bill_amount,
        "BILL_VOLUME": bill_volume
    }])

    # Predictions & Probabilities
    prediction = pipeline.predict(input_data)
    cluster = int(prediction[0])
    probs = pipeline.predict_proba(input_data)[0]
    prob = float(probs[cluster])

    input_data["Cluster"] = cluster
    input_data["Insights"] = cluster_insights.get(cluster, "No insight available")

    # Show main result
    st.success(f"This customer is most likely in **Cluster {cluster}** with probability {probs[cluster]:.2%}")

    # Show probability breakdown as DataFrame
    prob_df = pd.DataFrame([probs], columns=[f"Cluster {i}" for i in range(len(probs))])
    st.write("### Probability Breakdown")
    st.dataframe(prob_df.T.rename(columns={0: "Probability"}))

    # Pie Chart for probabilities
    fig, ax = plt.subplots()
    ax.pie(probs, labels=[f"Cluster {i}" for i in range(len(probs))],
           autopct="%1.1f%%", startangle=90, colors=["#66b3ff", "#99ff99", "#ffcc99"])
    ax.axis("equal")
    st.pyplot(fig)

        # Recommendations
    if cluster == 0:
        st.warning("Recommendation: Promote water conservation awareness programs in households. Monitor for leaks but overall low risk.")
    elif cluster == 1:
        st.warning("Recommendation: Ensure billing compliance for SMEs. Encourage efficient water use practices.")
    elif cluster == 2:
        st.warning("Recommendation: Prioritize smart metering for farms and irrigation areas. Investigate for possible non-revenue water losses (illegal use or leaks).")
    elif cluster == 3:
        st.warning("Recommendation: Closely monitor industrial users for efficiency and compliance. Consider tailored tariffs or stricter oversight.")


    # CSV download
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
    "Upload a CSV file with WATER_AMOUNT, SEWER_AMOUNT, BILL_AMOUNT and BILL_VOLUME columns",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("📋 Uploaded Data Preview:")
    st.dataframe(data.head())

    try:
        predictions = pipeline.predict(data[["WATER_AMOUNT", "SEWER_AMOUNT", "BILL_AMOUNT", "BILL_VOLUME"]])
        probas = pipeline.predict_proba(data[["WATER_AMOUNT", "SEWER_AMOUNT", "BILL_AMOUNT", "BILL_VOLUME"]])

        data["Cluster"] = predictions
        for i in range(probas.shape[1]):
            data[f"Cluster_{i}_prob"] = probas[:, i]
        data["Insights"] = data["Cluster"].map(cluster_insights)

        st.success("✅ Clusters assigned successfully!")
        st.dataframe(data.head())

        # CSV Download
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
        st.error(f"Error during batch prediction: {e}")



st.markdown("---")
st.markdown("### 📬 Contact")
st.write("👩‍💻 Developed by **Group3**")
st.write("✉️ Email: veesandra30@gmail.com")
st.write("[🌐 GitHub](https://github.com/Assesa44/water-loss-reduction-through-smart-metering.git)")
