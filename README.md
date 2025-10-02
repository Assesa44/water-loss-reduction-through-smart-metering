# **Nairobi Water Loss Analysis & Clustering**
## **Business Understanding**
### **Background**
The Nairobi City Water and Sewerage Company (NCWSC), responsible for supplying clean and safe water to Nairobi residents, despite heavily investing in water infrastructure, struggles with non-revenue water (NRW), water that is produced but not billed due to physical losses (leakages, illegal connections) and commercial losses (meter inaccuracies, billing errors).

According to the Water Services Regulatory Board (WASREB), NCWSC loses nearly 50% of the water it produces. This situation leads to:
- Reduced revenue and financial instability.

- Inefficient use of already scarce water resources.

- Constraints on sustaining infrastructure improvements.

### **Project Overview**
This project analyzes water consumption and billing data from Nairobi to detect non-revenue water (NRW) and potential water losses. It focuses on applying clustering models such as K-Means and Gaussian Mixture Models (GMM) to segment consumers based on billing, sewer, and water usage, as well as applying predictive modeling to help predict which billing category a new customer falls into.

This project's ultimate goal is to support smart metering strategies and provide actionable insights to reduce water loss.

### **STAKEHOLDERS**
Some of the major stakeholders include;

- NCWSC Management & Operations Teams – oversee production, distribution, and billing; directly responsible for reducing non-revenue water.

- Policy Makers & Regulators (e.g., WASREB, Ministry of Water & Sanitation) – set compliance standards, monitor performance, and allocate resources.

- Nairobi City Planners & County Government – align water management with urban development plans.

- Customers – end-users who rely on the water supply and are directly affected by service reliability, pricing, and billing accuracy.

- Technical Partners/Vendors – providers of smart metering technology and IoT solutions.

- Donors/Investors – external organizations funding or supporting water infrastructure projects.

---

## **Data Understanding**
### **Data Source**
The data used in this project was sourced from [Nairobi Water and Sewerage Company](https://portal.nairobiwater.co.ke/), and it contains details on the company's customers water usage data for 10 months.

The data in question can be downloaded [here](https://docs.google.com/spreadsheets/d/1Q2YkviN5tng_tSRmRjXlnA0Q85ofu8Qy/edit?usp=drive_link&ouid=110570190886409143359&rtpof=true&sd=true).

---

## **Data Preparation**
We followed best practices to prepare the data:

### 1. **Cleaning**

* Handled missing values
* Converted records to their correct data types
* Dropped uninformative columns

### 2. **Encoding**

* Categorical variables with:

  * **OneHot Encoding** 

### 3. **Standardizing**

* Standardized our numeric columns 

### 4. **Dimension Reduction**

* Reduced the dimensions of some of the columns using `PCA`

---

## **Modeling**
We tested multiple models and tuned them iteratively:

### 1. **KMeans Clustering**

* Performed KMeans Clustering iteratively, using the elbow method to choose the best n_clusters, PCA to reduce dimensionality (performed well)

### 2. **Gaussian Model (GMM)**

* Performed GMM to effectively improve our model by adding probabilities to the outputs, selected the best model using;
   - BIC (Bayesian Information Criterion)
   - AIC (Akaike Information Criterion)

* Unfortunately, this model did not work as expected, so we dropped it.

### 3. **Predictive Modeling** 

* Applied predictive modeling to help predict which billing category a new customer falls into.

### Evaluation Metrics

* **Silhouette Score** - measures how similar an object is to its own cluster compared to other clusters

* **Calinski-Harabasz Index**- measures the ratio of between-cluster separation to within-cluster compactness

* **Davies-Bouldin Index** - measures the average similarity between each cluster and its most similar one

---

## **Evaluation**

### **Final Model Performance**
- `Silhouette Score= 0.8108`, this indicates that the clusters are very well-separated and internally consistent. Before PCA, our silhouette was 0.80, which clearly indicates that PCA has improved cohesion + separation dramatically.

- `Calinski-Harabasz Index= 199495.90`, the higher the index, the better separation between clusters relative to within-cluster variance. At first, this might look like a drop in “quality,” but  PCA reduced dimensionality, often lowers absolute CH values.

- `Davies-Bouldin Index= 0.5216`, the closer to 0 the index is, the better it is. This indicates that the clusters are compact and farther away from each other.

---

## **Insights & Recommendations**
This section outlines key findings from the analysis and offers actionable recommendations for stakeholders, particularly the NCWSC board.


### Key Insights

```
🗂️ Repository Structure
├── Data/                # Raw and processed datasets (not uploaded here for privacy)
├── notebooks/           # Jupyter notebooks
│   ├── nairobi_water_loss.ipynb   # Main analysis & modeling notebook
├── README.md            # Project documentation (this file)
├── requirements.txt     # Python dependencies
```
⚙️ Setup Instructions
1️⃣ Clone the repository
``` bash
git clone https://github.com/Assesa44/nairobi-water-loss.git
cd nairobi-water-loss
```

2️⃣ Create and activate a virtual environment
``` bash
python -m venv venv
source venv/bin/activate      # On Mac/Linux
venv\Scripts\activate         # On Windows
```

3️⃣ Install dependencies
``` bash
pip install -r requirements.txt
```

``` bash
4️⃣ Launch Jupyter Notebook
jupyter notebook
```

Then open:

`notebooks/nairobi_water_loss.ipynb`

📊 Project Workflow
🔹 Data Understanding

Explore water amount, sewer amount, and bill amount across 200,000+ consumers.

Identify missing values, duplicates, and outliers.

🔹 Data Preparation

Feature scaling using StandardScaler.

Feature engineering (derived ratios between bill, water, and sewer amounts).

Filtering out anomalies for cleaner clustering results.

🔹 Modeling & Clustering

Baseline model with K-Means.

Model tuning using GridSearchCV with silhouette scoring.

Gaussian Mixture Models (GMM) for soft clustering and probability-based segmentation.

🔹 Evaluation Metrics

Silhouette Score

Calinski-Harabasz Index

Davies-Bouldin Index

🔹 Insights

Cluster 0: Majority of consumers, low individual contribution.

Cluster 1: Small group, but heavy revenue contributors (likely industries).

Cluster 2: Smaller niche, still high bills (possible estates or premium consumers).

🛠️ Tech Stack

Python

Pandas, NumPy for data manipulation

Matplotlib, Seaborn for visualization

Scikit-learn for clustering & pipelines

Jupyter Notebook for analysis

🚀 How to Reproduce Results

Open the notebook nairobi_water_loss.ipynb.

Run all cells in order.

The notebook will:

Preprocess the data

Apply clustering models

Visualize clusters and report metrics

📌 Recommendations

Rollout smart metering for Cluster 1 (industries) to monitor high-value consumers.

Investigate non-revenue water in Cluster 0 where consumer count is large but individual bills are low.

Use probability-based segmentation (GMM) for more flexible consumer classification.

🤝 Contribution

Fork the repo

Create a new branch: git checkout -b feature-name

Commit your changes: git commit -m "Add new feature"

Push to the branch: git push origin feature-name

Submit a pull request

📄 License

This project is licensed under the MIT License.
