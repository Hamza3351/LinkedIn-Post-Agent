**AI Job Match Analyzer**
==============================
<p align="center">
  <img src="https://img.shields.io/badge/LLM-Llama3.1_70B-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-LPU_Inference-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge" />
</p>

A **high-precision NLP + LLM-powered analyzer** that compares a **Job Description** and a **Resume**, extracts skills, computes match %, identifies gaps, and generates **AI-optimized resume improvement suggestions** powered by **Groq’s ultra-fast Llama 3.1 70B**.

---

## 🚀 **Features**
- **Extracts skills & keywords** (spaCy + custom parsing)
  
- Computes:
  - **Match %**
  - **Missing Skills**
  - **Matched Skills**
  - **Resume Score**
    
- Generates:
  - **3 Resume Bullet Suggestions**
  - **1 Professional Headline**
  - **1 Rationale Summary**
    
- Modern **Streamlit UI** with color-coded sections & skill badges

- **Fully free** (no paid APIs) — uses **Groq free tier**

---
    
## 🧰 **Tech Stack**
| Component | Used For |
|----------|----------|
| **Python 3.10+** | Core logic |
| **spaCy** | NLP skill extraction |
| **RapidFuzz** | Fuzzy skill matching |
| **Groq API (Llama 3.1 70B)** | Resume suggestions |
| **Streamlit** | Frontend UI |
| **Inline CSS + HTML** | Custom styling |

---

## 📂 **Project Structure**
```
 ai_job_analyzer/
│── analyzer.py          
│── model_interface.py   
│── app.py               
│── requirements.txt
│── examples/
│     └── job_desc.txt
|     └── resume.txt
│── README.md
```


---

## 🖥️ **How It Works**

### **1️⃣ Skill Extraction**
✔ Noun chunks  
✔ Entities  
✔ Token-based filtering  
✔ Normalization + cleaning  

---

### **2️⃣ Skill Matching (JD → Resume)**
Uses **RapidFuzz** token-sort ratio to compute:

- Match %
- Missing skills
- Matched pairs

---

### **3️⃣ AI Suggestion Generation**
Groq Llama 3.1 70B produces:

- 3 resume bullets (10–15 words)
- A strong headline
- A rationale explaining the match score

---

### **4️⃣ UI Presentation**
Streamlit displays:

- Extracted skills  
- Missing skills as colored badges  
- Match %  
- Resume score  
- AI recommendations  

---

## ▶️ **Run Locally**

### **Install Dependencies**
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
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

## 📝 **Example Inputs**

### Job Description (JD)
```
We are seeking a Senior Data Engineer with 5+ years of experience in Python development and data engineering. 
The candidate should have experience with cloud-based solutions, building scalable data pipelines, 
working with cross-functional teams, ETL workflows, and ensuring data quality, integrity, and performance. 
Strong knowledge of distributed systems, automated testing, CI/CD pipelines, and production deployments 
on cloud platforms (AWS, GCP, or Azure) is required. Familiarity with data applications, documentation 
of technical specifications and best practices, relational databases, NoSQL databases (MongoDB), 
REST APIs, microservices, message queues (Kafka), cloud infrastructure, DevOps tools, Kubernetes, Terraform, 
and other CI/CD tools is strongly preferred.
```

### Resume
```
I am a software engineer with 3 years of experience in Python and SQL. 
I have built ETL pipelines, used Docker and Kubernetes for containerized deployment, 
and deployed small-scale data applications on AWS. I am familiar with relational databases, 
basic CI/CD pipelines, and some cloud infrastructure tools. I have collaborated with small teams 
on several projects, focusing on data processing and analysis.
```
---

## ⭐ **Future Improvements**

*   Skill ontology mapping
*   Support for PDF/Docx uploads
*   ATS score
*   Resume rewriting
*   Multi-language support
---

## 🤝 **Contributing**

Pull requests are welcome!\
If you want to extend this into a SaaS product, feel free to reach out.

---

## 📹 **Demo Video**

Coming soon on YouTube 📺

---

## 📬 **Contact**

For customization or freelance work, reach out anytime.

---

## 📄 **License**

MIT
