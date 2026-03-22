import streamlit as st
import pdfplumber
import json
from groq import Groq
from pydantic import BaseModel, Field
from typing import List, Optional

# --- LOAD FROM SECRETS ---
GROQ_API_KEY = st.secrets["api_key"]
MODEL_NAME = st.secrets["model"]
MAX_PDF_PAGES = st.secrets["max_pdf_pages"]
MAX_TEXT_LENGTH = st.secrets["max_text_length"]
SYSTEM_PROMPT_BASE = st.secrets["system_prompt"]
SECURITY_PROMPT_BASE = st.secrets["security_prompt"]
TEMPERATURE = st.secrets["temperature"]
SEED = st.secrets["seed"]

# --- 1. DATA MODELS ---
class Metric(BaseModel):
    score: int = 0
    critique: str = ""

class Character(BaseModel):
    name: str = ""
    archetype: str = ""
    motivation: str = ""
    fatal_flaw: str = "" 
    market_potential: str = ""

class SceneBeat(BaseModel):
    title: str = ""
    summary: str = ""
    tension: int = 0
    emotional_shift: str = ""
    script_doctor_note: str = ""

class Cliffhanger(BaseModel):
    line: str = ""
    logic: str = ""

class ScriptAudit(BaseModel):
    is_narrative: bool = False
    is_presentable: bool = False
    rejection_reason: str = "Invalid Content"
    summary: str = ""
    engagement_score: int = 0
    hook: Metric = Metric()
    dialogue: Metric = Metric()
    pacing: Metric = Metric()
    comparable_hit: str = "" 
    market_benchmark_reason: str = ""
    audience_demographic: str = ""
    characters: List[Character] = []
    scenes: List[SceneBeat] = []
    cliffhangers: List[Cliffhanger] = []
    improvements: List[str] = []

# --- 2. THE ENGINE ---
class BulletEngine:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

    def get_text(self, file):
        if hasattr(file, 'type') and file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                text = "\n".join([p.extract_text() or "" for p in pdf.pages[:MAX_PDF_PAGES]])
                return text[:MAX_TEXT_LENGTH]
        content = file if isinstance(file, str) else str(file.read(), "utf-8")
        return content[:MAX_TEXT_LENGTH]

    def analyze(self, text: str):
        json_template = {
            "is_narrative": True, "is_presentable": True, "rejection_reason": "None",
            "summary": "...", "engagement_score": 0,
            "hook": {"score": 0, "critique": "..."},
            "dialogue": {"score": 0, "critique": "..."},
            "pacing": {"score": 0, "critique": "..."},
            "comparable_hit": "Title",
            "market_benchmark_reason": "Analysis vs Tiers.",
            "audience_demographic": "Demographic string.",
            "characters": [{"name": "...", "archetype": "...", "motivation": "...", "fatal_flaw": "...", "market_potential": "..."}],
            "scenes": [{"title": "Scene 1", "summary": "...", "tension": 50, "emotional_shift": "...", "script_doctor_note": "..."}],
            "cliffhangers": [{"line": "...", "logic": "..."}],
            "improvements": ["Note"]
        }

        system_prompt = SYSTEM_PROMPT_BASE + f"\nOUTPUT TEMPLATE:\n{json.dumps(json_template)}"
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text[:MAX_TEXT_LENGTH]}
            ],
            model=self.model,
            response_format={"type": "json_object"},
            temperature=TEMPERATURE,
            seed=SEED
        )
        return json.loads(response.choices[0].message.content)

    def chat_grounded(self, query, context, history):
        security_sys = SECURITY_PROMPT_BASE + f"\nSOURCE SCRIPT:\n{context[:4000]}"

        reinforced_user_query = f"{query}\n\n(Reminder: Discuss the script quality and improvements only.)"

        msgs = [
            {"role": "system", "content": security_sys},
            *history,
            {"role": "user", "content": reinforced_user_query}
        ]
        
        res = self.client.chat.completions.create(
            messages=msgs,
            model=self.model,
            temperature=0
        )
        return res.choices[0].message.content