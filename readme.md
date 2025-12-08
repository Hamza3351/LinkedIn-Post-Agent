**LinkedIn Post Agent**
==============================
<p align="center">
  <img src="https://img.shields.io/badge/LLM-Llama3.3_70B-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-LPU_Inference-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge" />
</p>

A **LinkedIn content generation tool** that produces **5 variations of posts**, each with attention-grabbing **hooks**, a well-structured **post body**, and strong **CTAs**, powered by **Groq’s ultra-fast llama-3.3-70b-versatile**.

---

## 🚀 **Features**
- Generates **5 unique LinkedIn post variations** at once

- Each variation includes:
  - **3 Hooks** for attention
  - **1 Post Body** (100–180 words, storytelling optimized)
  - **2 CTAs** (Call to Actions)

- Optional **JSON output** for developers

- **Download as TXT or PDF**

- Fully Python + Streamlit — no complex setup

---
    
## 🧰 **Tech Stack**
| Component | Used For |
|----------|----------|
| **Python 3.10+** | Core logic |
| **Groq API (llama-3.3-70b-versatile)** | AI content generation |
| **Streamlit** | Frontend UI |
| **FPDF** | PDF generation |
| **Inline CSS + HTML** | Custom styling |

---

## 📂 **Project Structure**
```
linkedin_post_agent/
│── app.py               
│── requirements.txt
│── README.md
```

---

## 🖥️ **How It Works**

### **1️⃣ Generate Posts**
✔ Enter a **Topic**, **Tone**, and **Target Audience**  
✔ Click **Generate Posts**  

---

### **2️⃣ Post Variations**
The agent creates 5 variations with:

- 3 Hooks  
- 1 Post Body  
- 2 CTAs  

---

### **3️⃣ Download Options**
- TXT file with all variations  
- PDF file with clean formatting and left-aligned headings  
- Optional JSON output for advanced use

---

### **4️⃣ Streamlit UI**
- Sidebar inputs for topic, tone, and audience  
- Expandable sections for each variation  
- Download buttons for TXT/PDF  
- Optional JSON viewer

---

## ▶️ **Run Locally**

### **Install Dependencies**
```
pip install -r requirements.txt
```

---

### **Launch the Streamlit App**
```
streamlit run app.py
```

---

## 🔑 **Setup Groq API Key**
</br>

>[!IMPORTANT]
>You must set your Groq API key as an environment variable.
>If you get any model error, you need to update the model version as they get decommissioned

</br>
Login to your groq dashborad and then create new API key. Copy that key and then set it as an environment variable using:

### **Mac/Linux (bash/zsh)**
```
export GROQ_API_KEY="your_api_key_here" 
```
### **Windows Powershell**
```
setx GROQ_API_KEY "your_api_key_here" 
```

After that Then restart your terminal and verify:
```
echo $env:GROQ_API_KEY
```
---

## 📝 **Example Input**
### Topic
```
How AI agentic workflows can boost freelancer productivity
```
### Tone
```
Expert, friendly, storytelling
```
### Audience
```
Freelancers, creators, LinkedIn users
```

---

## ⭐ **Future Improvements**

* Multi-language support  
* AI-powered content scheduling  
* LinkedIn auto-post integration  
* Advanced formatting options in PDF  
* SaaS-ready version  

---

## 🤝 **Contributing**

Pull requests welcome!\
If you want to help improve this tool or build a SaaS version, reach out.

---

## 📹 **Demo Video**

Coming soon on YouTube 📺

---

## 📬 **Contact**

For customization or freelance work, reach out anytime.

---

## 📄 **License**

MIT
