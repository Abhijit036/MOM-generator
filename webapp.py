import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor
from docxextractor import extract_text_from_docx
from imageextractor import extract_text_from_image
from streamlit_lottie import st_lottie
import requests

# ------------------------- Helper Functions -------------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ------------------------- Lottie Animations -------------------------
upload_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")
processing_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_usmfx6bp.json")
success_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# ------------------------- Configure GenAI -------------------------
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ------------------------- App Config -------------------------
st.set_page_config(page_title="AI MOM Generator", page_icon="📝", layout="wide")

st.markdown("<h1 style='text-align: center; color: orange;'>📝 AI-assisted Minutes of Meeting Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: green;'>Professional MoM in seconds</h4>", unsafe_allow_html=True)
st.write("---")

# ------------------------- Sidebar -------------------------
st.sidebar.header("📂 Upload Your MOM Notes")
st.sidebar.markdown("Upload your meeting notes in **PDF, DOCX, or Image format**.")
st_lottie(upload_animation, height=200, key="upload")

user_file = st.sidebar.file_uploader("Choose your file", type=['pdf', 'docx', 'png', 'jpg', 'jpeg'])

user_text = None
if user_file is not None:
    if user_file.type == "application/pdf":
        user_text = text_extractor(user_file)
    elif user_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        user_text = extract_text_from_docx(user_file)
    elif user_file.type in ["image/png", "image/jpg", "image/jpeg"]:
        user_text = extract_text_from_image(user_file)

    if user_text:
        st.sidebar.success("✅ File uploaded successfully!")

# ------------------------- Tabs -------------------------
tab1, tab2, tab3 = st.tabs(["📤 Upload Notes", "📜 Generated MoM", "📝 Summary"])

with tab1:
    st.subheader("💡 Instructions")
    st.markdown("""
    1. Upload your meeting notes in **PDF, DOCX, or Image** format.  
    2. Click **Generate MoM** in the Generated MoM tab.  
    3. Download or copy the MoM after it is generated.
    """)

with tab2:
    if st.button('🚀 Generate MoM'):
        if not user_text:
            st.error("❌ No text extracted. Please upload a valid file.")
        else:
            with st.spinner("⏳ Generating your professional MoM..."):
                prompt = f"""
                Assume you are an expert in creating minutes of meeting. 
                User has provided notes of a meeting in text format. Using this data you need to create a standardized 
                minutes of meeting. The data provided by user is as follows: {user_text}

                Keep the format strictly as mentioned below:

                **Title:** Title of meeting  
                **Heading:** Meeting Agenda  
                **Subheading:** Name of the attendees (If not present, write NA)  
                **Subheading:** Date and place of meeting (If place not provided, keep it as Online)  

                **Body:** The body must follow this sequence:
                - KEY POINTS DISCUSSED  
                - HIGHLIGHT any decision that has been finalized  
                - Mention actionable items  
                - Any additional notes  
                - Any deadlines that have been discussed  
                - Next meeting date (if mentioned)  
                - 2-3 line summary  

                Use **bullet points** and highlight/format important keywords for clarity.  
                """

                response = model.generate_content(prompt)
                mom_text = response.text

            st_lottie(success_animation, height=150)
            st.success("✅ MoM Generated Successfully!")

            # Collapsible MoM
            st.subheader("📜 Generated Minutes of Meeting")
            for section in mom_text.split("\n\n"):
                with st.expander(section[:50]+"..."):
                    st.write(section)

            # Copy and Download Buttons
            st.download_button(
                label="💾 Download MoM as TXT",
                data=mom_text,
                file_name="generated_minutes_of_meeting.txt",
                mime="text/plain"
            )
            st.code(mom_text, language="text")
            st.button("📋 Copy to Clipboard", on_click=lambda: st.experimental_set_query_params(mom_text=mom_text))

with tab3:
    st.subheader("📝 MoM Summary")
    if user_text:
        with st.spinner("Summarizing..."):
            summary_prompt = f"Provide a concise 3-line professional summary of this meeting notes:\n\n{user_text}"
            summary_response = model.generate_content(summary_prompt)
        st.info(summary_response.text)
    else:
        st.warning("Upload a file in the Upload tab first.")
