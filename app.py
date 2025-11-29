import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Custom App Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f2ec; /* warm beige background */
    }

    [data-testid="stSidebar"] {
        background-color: #faf9f6; /* slightly lighter sidebar */
        color: #000000;
    }

    h1, h2, h3 {
        color: #2b2b2b; /* dark gray text for contrast */
    }

    .stButton>button {
        background-color: #00338d; /* KPMG blue for accents */
        color: white;
        border-radius: 8px;
        border: none;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #002a73;
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load summary data from CSV
df = pd.read_csv("summary_data.csv")

# Calculate a combined ROI sustainability score 
df["roi_sustainability_score"] = df["roi_tokens_per_dollar"] / df["co2_g"]

# Display the KPMG logo centered
st.image("KPMG_logo.png", width=250)


st.title(" LLM ROI & Sustainability Dashboard")
st.write("Compare LLM models by Cost, CO₂ Emissions, Energy, and ROI")

# Sidebar for metric selection
metric = st.sidebar.selectbox(
    "Select a metric to visualize",
    ["cost_usd", "co2_g", "energy_Wh", "energy_Wh_per_token", "roi_tokens_per_dollar", "roi_sustainability_score"]
)

# Barplot for selected metric
st.subheader(f"{metric} by Model")
fig, ax = plt.subplots()
sns.barplot(data=df.sort_values(metric, ascending=False), x=metric, y="model_name", ax=ax)
st.pyplot(fig)

# Scatter plot for tradeoffs
st.subheader(" Tradeoff: Cost vs CO₂ Emissions")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="cost_usd", y="co2_g", hue="model_name", s=100)
for i in range(df.shape[0]):
    ax2.text(df["cost_usd"][i], df["co2_g"][i], df["model_name"][i])
ax2.set_xlabel("Cost (USD)")
ax2.set_ylabel("CO₂ Emissions (g)")
st.pyplot(fig2)


