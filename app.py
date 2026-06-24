import streamlit as st
import requests
from PIL import Image
from dotenv import load_dotenv
from plant_care import PLANT_CARE
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# -------------------------
# Page Settings
# -------------------------

st.set_page_config(
    page_title="GardenGPT",
    page_icon="🌱",
    layout="centered"
)

st.markdown("""
<style>

.hero {
    text-align: center;
    padding: 18px;
    border-radius: 15px;
    background: linear-gradient(
        135deg,
        #1e3c2d,
        #2d5a40
    );
    color: white;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 5px;
}

.hero h3 {
    margin-top: 0px;
}

.feature-card {
    padding: 12px;
    border-radius: 10px;
    background-color: #262730;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)
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
    st.sidebar.success(
    "🚀 Live on Streamlit Cloud"
)
    st.sidebar.info(
    "📦 Powered by PlantNet API"
)

# -------------------------
# Header
# -------------------------

st.markdown("""
<div class="hero">

<h1> 🌱 GardenGPT</h1>

<h3>Your Personal AI Gardening Assistant</h3>

<p>
Identify plants instantly and receive intelligent care recommendations.
</p>

</div>
""", unsafe_allow_html=True)
st.divider()

st.markdown("""
<div class="feature-card">
🪴 <b>Plant Identification</b><br>
Identify thousands of plants instantly.
</div>

<div class="feature-card">
💧 <b>Water Recommendations</b><br>
Learn proper watering schedules.
</div>

<div class="feature-card">
☀️ <b>Sunlight Guidance</b><br>
Understand ideal lighting conditions.
</div>

<div class="feature-card">
🌱 <b>Soil Advice</b><br>
Get suitable soil recommendations.
</div>
""", unsafe_allow_html=True)

# -------------------------
# Report Generator
# -------------------------

def create_pdf_report(
    plant_name,
    common_names,
    family,
    genus,
    confidence,
    care_info
):

    filename = "GardenGPT_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("GardenGPT Plant Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Scientific Name:</b> {plant_name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Common Names:</b> {', '.join(common_names)}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Family:</b> {family}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Genus:</b> {genus}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Confidence:</b> {confidence:.2f}%",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    if care_info:

        content.append(
            Paragraph(
                "Plant Care Guide",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Water:</b> {care_info['water']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Sunlight:</b> {care_info['sunlight']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Soil:</b> {care_info['soil']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Fertilizer:</b> {care_info['fertilizer']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Fun Fact:</b> {care_info['fun_fact']}",
                styles["BodyText"]
            )
        )

    doc.build(content)

    return filename

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

            # -------------------------
            # Plant Information
            # -------------------------

            st.markdown("## 🪴 Plant Information")

            st.info(
                f"""
Scientific Name: {plant_name}

Common Names: {', '.join(common_names)}

Family: {family}

Genus: {genus}
"""
            )

            # Metrics Row

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Confidence",
                    f"{confidence:.1f}%"
                )

            with col2:
                st.metric(
                    "Family",
                    family
                )

            with col3:
                st.metric(
                    "Genus",
                    genus
                )

            # -------------------------
            # Care Guide
            # -------------------------

            if care_info:

                st.markdown("## 🌿 Plant Care Guide")

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
# Download Button
# -------------------------

            pdf_file = create_pdf_report(
                plant_name,
                common_names,
                family,
                genus,
                confidence,
                care_info
            )

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📄 Download Plant Report",
                    data=file,
                    file_name="GardenGPT_Report.pdf",
                    mime="application/pdf"
                )
# -------------------------
# Footer
# -------------------------

st.divider()

st.caption(
    "GardenGPT • Built with Python, Streamlit and PlantNet API"
)