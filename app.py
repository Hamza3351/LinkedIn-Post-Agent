import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from io import BytesIO
from fpdf import FPDF
import re

load_dotenv()

#Make sure you set your API key as an environment variable using:
#export GROQ_API_KEY="your_api_key_here" (Linux/Mac)
#setx GROQ_API_KEY "your_api_key_here" (Windows)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a LinkedIn Content Agent specialized in generating highly engaging posts.

For every request:
1. Create 5 complete LinkedIn post variations.
2. Each variation must include:
   - 3 high-retention hooks
   - 1 post body (100–180 words unless user requests otherwise)
   - 2 strong CTAs
3. Style must be optimized for:
   • storytelling
   • clarity
   • virality
   • emoji-light but engaging
4. Use the user's niche and audience clearly inside the content.

Return everything in clean JSON:
{
  "variations": [
    {
      "hooks": ["...", "...", "..."],
      "post": "...",
      "ctas": ["...", "..."]
    }
  ]
}
"""

#Helper Functions
def clean_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        if "```" in raw:
            raw = raw.split("```")[0]
    return raw.strip()

def wrap_text_for_pdf(text, max_len=50):
    """
    Ensures no single word is longer than max_len.
    Removes control characters and inserts breakable spaces.
    """
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", text)

    def break_word(match):
        word = match.group(0)
        return "\u200b".join([word[i:i+max_len] for i in range(0, len(word), max_len)])

    return re.sub(r'\S{' + str(max_len+1) + r',}', break_word, text)

def generate_posts(topic, tone, audience):
    user_prompt = f"""
    Topic: {topic}
    Tone: {tone}
    Audience: {audience}
    Generate LinkedIn posts.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        max_tokens=2500
    )
    result = response.choices[0].message.content
    cleaned = clean_json(result)
    try:
        parsed = json.loads(cleaned)
        return parsed, cleaned
    except:
        return None, cleaned

def create_txt(data):
    txt = ""
    for i, item in enumerate(data["variations"], 1):
        txt += f"Variation {i}\n"
        txt += "Hooks:\n" + "\n".join(f"- {h}" for h in item["hooks"]) + "\n"
        txt += f"Post:\n{item['post']}\n"
        txt += "CTAs:\n" + "\n".join(f"- {c}" for c in item["ctas"]) + "\n"
        txt += "-"*40 + "\n"
    return txt

def create_pdf(data):
    MAX_WIDTH = 180  
    LEFT_MARGIN = 15

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_left_margin(LEFT_MARGIN)
    pdf.set_font("Arial", size=12)

    for i, item in enumerate(data["variations"], 1):
        pdf.set_font("Arial", "B", 14)
        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(MAX_WIDTH, 7, wrap_text_for_pdf(f"Variation {i}"))
        pdf.ln(8)

        pdf.set_font("Arial", "", 12)
        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(MAX_WIDTH, 7, wrap_text_for_pdf("Hooks:\n" + "\n".join(f"- {h}" for h in item["hooks"])))
        pdf.ln(8)

        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(MAX_WIDTH, 7, wrap_text_for_pdf(f"Post:\n{item['post']}"))
        pdf.ln(8)

        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(MAX_WIDTH, 7, wrap_text_for_pdf("CTAs:\n" + "\n".join(f"- {c}" for c in item["ctas"])))

        pdf.ln(15)  

    pdf_bytes = pdf.output(dest='S')
    return BytesIO(pdf_bytes)

#Streamlit App
st.set_page_config(page_title="LinkedIn Post Agent", layout="wide")
st.title("LinkedIn Post Generator (Llama 3)")
st.write("Generate 5 powerful LinkedIn posts with hooks and CTAs.")

with st.sidebar:
    st.header("Settings")
    topic = st.text_area("Post Topic", placeholder="e.g., How AI agents change freelancing")
    tone = st.selectbox("Tone", ["expert", "friendly", "bold", "storytelling", "direct"])
    audience = st.text_input("Target Audience", placeholder="founders, job seekers, creators")
    show_json = st.checkbox("Show JSON Output (optional)")
    generate_btn = st.button("Generate Posts", use_container_width=True)

if generate_btn:
    if not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating posts using Llama 3…"):
            data, raw = generate_posts(topic, tone, audience)

        if data is None:
            st.error("Model returned invalid JSON. Showing raw output.")
            st.code(raw)
        else:
            st.success("Posts generated successfully!")

            for i, item in enumerate(data["variations"], 1):
                with st.expander(f"🔵 Variation {i}", expanded=True):
                    st.markdown("### 🔥 Hooks")
                    for hook in item["hooks"]:
                        st.write(f"- {hook}")

                    st.markdown("### ✍️ Post")
                    st.write(item["post"])

                    st.markdown("### 📣 CTAs")
                    for cta in item["ctas"]:
                        st.write(f"- {cta}")

            st.download_button(
                label="💾 Download as TXT",
                data=create_txt(data),
                file_name="linkedin_posts.txt",
                mime="text/plain"
            )

            st.download_button(
                label="💾 Download as PDF",
                data=create_pdf(data),
                file_name="linkedin_posts.pdf",
                mime="application/pdf"
            )

            if show_json:
                st.subheader("Raw JSON Output")
                with st.expander("Click to view JSON"):
                    st.code(raw, language="json")
