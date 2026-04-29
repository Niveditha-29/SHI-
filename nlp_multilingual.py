from sentence_transformers import SentenceTransformer, util
from dateutil import parser as dateparser
import re
from typing import Tuple, Dict

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SIMILARITY_THRESHOLD = 0.55
FALLBACK_INTENT = "unknown_fallback"

TEMPLATES = [
    {"intent": "get_groundwater_level", "text_en": "What is the groundwater level in Pune today?", "text_hi": "आज पुणे में भूजल स्तर क्या है?"},
    {"intent": "get_groundwater_trend", "text_en": "Show groundwater trend for Pune last 3 months", "text_hi": "पिछले 3 महीनों का भूजल प्रवृत्ति दिखाइए"},
    {"intent": "submit_report", "text_en": "I want to submit a water quality report", "text_hi": "मैं water quality रिपोर्ट जमा करना चाहता हूँ"},
    {"intent": "faq_irrigation", "text_en": "Tell me about irrigation schemes in my district", "text_hi": "मेरे जिले में सिंचाई योजनाओं के बारे में बताइए"},
    {"intent": "greet", "text_en": "hello", "text_hi": "नमस्ते"},
    {"intent": "goodbye", "text_en": "bye", "text_hi": "अलविदा"},
    {"intent": "help", "text_en": "help me", "text_hi": "मदद करें"}
]

DISTRICT_LIST = ["pune","mumbai","bangalore","hyderabad","nagpur","ahmedabad","chennai","delhi","kolkata"]

MODEL = SentenceTransformer(MODEL_NAME)
_template_texts = []
_template_intents = []
for item in TEMPLATES:
    for k,v in item.items():
        if k.startswith("text_"):
            _template_texts.append(v)
            _template_intents.append(item["intent"])
TEMPLATE_EMB = MODEL.encode(_template_texts, convert_to_tensor=True, show_progress_bar=False)

def extract_district(text: str):
    txt = text.lower()
    for d in DISTRICT_LIST:
        if re.search(r"\b" + re.escape(d) + r"\b", txt):
            return d
    m = re.search(r"\bin\s+([A-Za-z\u0900-\u097f\u0c00-\u0c7f ]+)", txt)
    if m:
        return m.group(1).strip().split()[0]
    return None

def extract_date(text: str):
    txt = text.lower()
    if "today" in txt or "आज" in txt:
        return "today"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if m: return m.group(1)
    m2 = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", text)
    if m2:
        try:
            dt = dateparser.parse(m2.group(1), dayfirst=True)
            return dt.strftime("%Y-%m-%d")
        except:
            return m2.group(1)
    return None

def extract_report_slots(text: str):
    slots = {}
    m = re.search(r"site[:\s]+([A-Za-z0-9_\- ]+)", text, re.I)
    if m:
        slots["site"] = m.group(1).strip()
    m2 = re.search(r"sample[:\s]+([A-Za-z0-9_\-]+)", text, re.I)
    if m2:
        slots["sample_id"] = m2.group(1).strip()
    fields = {}
    for k,v in re.findall(r"([A-Za-z_]+)=([0-9.]+)", text):
        fields[k] = v
    if fields:
        slots["fields"] = fields
    date = extract_date(text)
    if date:
        slots["date"] = date
    return slots

def predict_intent_and_entities(text: str) -> Tuple[str, Dict, float]:
    if not text or not text.strip():
        return FALLBACK_INTENT, {}, 0.0
    emb = MODEL.encode(text, convert_to_tensor=True, show_progress_bar=False)
    hits = util.cos_sim(emb, TEMPLATE_EMB)[0]
    top_idx = int(hits.argmax().cpu().numpy())
    top_score = float(hits[top_idx].cpu().numpy())
    intent = _template_intents[top_idx]
    if top_score < SIMILARITY_THRESHOLD:
        return FALLBACK_INTENT, {}, top_score
    entities = {}
    if intent in ("get_groundwater_level", "get_groundwater_trend"):
        d = extract_district(text)
        if d:
            entities["district"] = d
        dt = extract_date(text)
        if dt:
            entities["date"] = dt
    elif intent == "submit_report":
        entities["slots"] = extract_report_slots(text)
    return intent, entities, top_score

