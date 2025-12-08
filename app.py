import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from io import BytesIO

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
    buffer = BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leading=15,
        alignment=TA_LEFT
    )

    story = []

    for i, item in enumerate(data["variations"], 1):

        story.append(Paragraph(f"Variation {i}", title_style))
        story.append(Paragraph("Hooks", section_style))

        for hook in item["hooks"]:
            story.append(Paragraph(f"- {hook}", body_style))

        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Post", section_style))
        story.append(Paragraph(item["post"], body_style))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("CTAs", section_style))

        for cta in item["ctas"]:
            story.append(Paragraph(f"- {cta}", body_style))
        story.append(Spacer(1, 0.4 * inch))

    pdf.build(story)
    buffer.seek(0)
    return buffer

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
