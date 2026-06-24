import streamlit as st
import requests
from PIL import Image
from dotenv import load_dotenv
from plant_care import PLANT_CARE
import os

# -------------------------
# Page Settings
# -------------------------

st.set_page_config(
    page_title="GardenGPT",
    page_icon="🌱",
    layout="centered"
)

# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("About")

    st.write("""
    GardenGPT is an AI-powered gardening assistant.

    Built using:
    - PlantNet API
    - Python
    - Streamlit

    Developed by Saif Khan.
    """)

# -------------------------
# Header
# -------------------------

st.markdown("""
# 🌱 GardenGPT

### AI-Powered Smart Gardening Assistant

Identify plants and receive intelligent care recommendations instantly.
""")

st.divider()

st.markdown("""
Upload a plant image and receive:

- Plant Identification
- Water Requirements
- Sunlight Requirements
- Soil Recommendations
- Fertilizer Suggestions
- Fun Facts
""")

# -------------------------
# File Upload
# -------------------------

uploaded_file = st.file_uploader(
    "Choose a plant image",
    type=["jpg", "jpeg", "png"]
)

# -------------------------
# Analysis
# -------------------------

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Plant",
        use_container_width=True
    )

    if st.button("Analyze Plant 🌿"):

        with st.spinner("GardenGPT is analyzing your plant..."):

            plantnet_key = os.getenv("PLANTNET_API_KEY")

            url = (
                f"https://my-api.plantnet.org/"
                f"v2/identify/all?api-key={plantnet_key}"
            )

            uploaded_file.seek(0)

            files = {
                "images": uploaded_file
            }

            response = requests.post(
                url,
                files=files
            )

            data = response.json()

            result = data["results"][0]

            plant_name = result["species"]["scientificName"]

            common_names = result["species"]["commonNames"]

            family = result["species"]["family"]["scientificName"]

            genus = result["species"]["genus"]["scientificName"]

            confidence = result["score"] * 100

            care_info = PLANT_CARE.get(plant_name)

            st.success("🌱 Plant Identified!")

            st.markdown("## 🪴 Plant Information")

            st.info(
                f"""
Scientific Name: {plant_name}

Common Names: {', '.join(common_names)}

Family: {family}

Genus: {genus}
"""
            )

            st.progress(
                min(confidence / 100, 1.0)
            )

            st.write(
                f"**Confidence Score:** {confidence:.2f}%"
            )

            st.markdown("## 🌿 Plant Care Guide")

            if care_info:

                st.success(
                    f"💧 Water: {care_info['water']}"
                )

                st.success(
                    f"☀️ Sunlight: {care_info['sunlight']}"
                )

                st.success(
                    f"🌱 Soil: {care_info['soil']}"
                )

                st.success(
                    f"🧪 Fertilizer: {care_info['fertilizer']}"
                )

                st.success(
                    f"✨ Fun Fact: {care_info['fun_fact']}"
                )

            else:

                st.warning(
                    "Plant identified, but no care guide exists yet."
                )

# -------------------------
# Footer
# -------------------------

st.divider()

st.caption(
    "GardenGPT • Built with Python, Streamlit and PlantNet API"
)