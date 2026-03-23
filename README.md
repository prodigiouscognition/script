# 🎬 Bullet | Production-Grade Script Intelligence

**Bullet** is an advanced narrative auditing and market-fit benchmarking tool designed for studio executives, producers, and screenwriters. Unlike standard LLM wrappers, Bullet utilizes a **Cynical Producer Persona** to evaluate scripts against real-world 2024-2026 market standards, providing deterministic scoring and deep structural diagnostics.

### 🚀 [Live Demo: Click Here to Test the App](https://scriptscoring.streamlit.app/)

---

## 🛠️ Technology Stack
* **Engine:** Python 3.9+
* **LLM Infrastructure:** Llama 3.3 70B (via **Groq Cloud** for ultra-fast inference)
* **Frontend:** Streamlit
* **Data Validation:** Pydantic (Strict Schema Enforcement)
* **Analytics & Visuals:** Plotly Express & Pandas
* **Document Processing:** PDFPlumber

---

## ✨ Key Features

### 1. The "Cynical Producer" Logic
Most AI models are programmed to be encouraging. Bullet is a tough studio executive. It uses a **Triple-Tier Benchmarking** system to compare your input against:
* **Global Blockbuster Level:** (e.g., *Inception*, *Mirzapur*, *Kalki 2898-AD*)
* **Average/Forgettable Hit Level:** (Generic procedural dramas or formulaic rom-coms)
* **Box Office Flop/Cringe Level:** (Fragments, textbook-style writing, or trope-heavy dialogue)

### 2. Deterministic Narrative Auditing
By utilizing a fixed `seed` and `temperature=0`, Bullet ensures that the same script receives the same score every time it is audited. This eliminates "LLM wobble" and provides reliable, repeatable data for production decisions.

### 3. Deep Narrative Diagnostics
* **Tension Mapping:** A scene-by-scene Plotly visualization of narrative stakes and emotional peaks.
* **Character Motivation Map:** Analyzes "Fatal Flaws," archetypes, and global marketability potential.
* **Retention Analysis:** Identifies viral "Cliffhanger" moments specifically for short-form or episodic content.

### 4. Grounded "Script Doctor" Chat
An ironclad RAG-based chat system that allows users to ask about script improvements. It is protected by a **Contextual Security Sandwich** to prevent prompt injections (e.g., it will strictly refuse to discuss history, science, or general knowledge, staying grounded in the provided script's universe).

---

## ⚖️ Engineering Decisions & Constraints

### 🪙 Token Constraint (5,000 Tokens)
For the current deployment, we have limited the analysis to the **first 25,000 characters (~5,000 tokens)**. 
* **Why?** This ensures API stability, prevents timeout errors on Streamlit Cloud, and maintains a high "Signal-to-Noise" ratio by focusing on the crucial setup and first act of the script.

### 🔄 Multi-Source Input Priority
The application features an explicit **Input Source Selector** to prevent "state stickiness" between uploaded PDFs, pasted text, and sample scripts.

---

## 📈 Future Roadmap

If granted additional development time, the following features are prioritized for the **V2.0 Release**:

1.  **Live IMDb Integration:** Instead of an internal reference database, the engine would fetch real-time IMDb ratings and box-office data for more granular market-fit comparisons.
2.  **Expanded Reference Library:** Loading 100+ "Certified Fresh" and "Certified Rotten" scripts from IMDb to use as direct few-shot references for more nuanced scoring.
3.  **Automated Script Coverage:** Generating industry-standard 2-page PDF "Producer Coverage" reports automatically.
4.  **Scene-Level Sentiment Analysis:** Utilizing NLP to track character emotional arcs more granularly across the entire script.

---

## 📦 Installation & Local Setup

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/your-username/bullet-intel.git](https://github.com/your-username/bullet-intel.git)
    cd bullet-intel
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Up Secrets:**
    Create a folder named `.streamlit` and a file inside name `secrets.toml`, add all the things that can't be shared publically like your keys, models and stuff.
    
5.  **Run the App:**
    ```bash
    streamlit run app.py
    ```
