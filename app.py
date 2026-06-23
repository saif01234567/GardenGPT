import streamlit as st
import requests
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from plant_care import PLANT_CARE
import os
st.set_page_config(
    page_title="GardenGPT",
    page_icon="🌱",
    layout="centered"
)

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Load Gemini model
#model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.title("🌱 GardenGPT")
with st.sidebar:

    st.header("About")

    st.write(
        """
        GardenGPT is an AI-powered gardening assistant.

        It uses:
        - PlantNet API
        - Python
        - Streamlit

        Developed by Saif Khan.
        """
    )

st.markdown("""
### AI-Powered Smart Gardening Assistant

Upload a plant image and receive:

- Plant Identification
- Water Requirements
- Sunlight Requirements
- Soil Recommendations
- Fertilizer Suggestions
- Fun Facts
""")

uploaded_file = st.file_uploader(
    "Choose a plant image",
    type=["jpg", "jpeg", "png"]
)

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

        url = f"https://my-api.plantnet.org/v2/identify/all?api-key={plantnet_key}"

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
        care_info = PLANT_CARE.get(plant_name)

        common_names = result["species"]["commonNames"]

        family = result["species"]["family"]["scientificName"]

        genus = result["species"]["genus"]["scientificName"]

        confidence = result["score"] * 100

        st.success("🌱 Plant Identified!")

        with st.container():

         st.subheader("Plant Information")

         st.write(f"**Scientific Name:** {plant_name}")

         st.write(f"**Common Names:** {', '.join(common_names)}")

         st.write(f"**Family:** {family}")

         st.write(f"**Genus:** {genus}")

        st.progress(min(confidence / 100, 1.0))

        st.write(f"**Confidence Score:** {confidence:.2f}%")
    
    if care_info:

        st.subheader("🌿 Plant Care Guide")

        st.write(f"**Water Requirements:** {care_info['water']}")

        st.write(f"**Sunlight Requirements:** {care_info['sunlight']}")

        st.write(f"**Soil Recommendations:** {care_info['soil']}")

        st.write(f"**Fertilizer Suggestions:** {care_info['fertilizer']}")

        st.write(f"**Fun Fact:** {care_info['fun_fact']}")