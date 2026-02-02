import os
import json
import google.generativeai as genai
from backend.app.engines.eda_engine import eda_engine
from backend.app.engines.ml_engine import ml_engine
from backend.app.engines.data_engine import data_engine
from dotenv import load_dotenv

load_dotenv()

HISTORY_FILE = "chat_history.json"

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.model = None
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        self.memory_store = self._load_history()

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.memory_store, f, indent=2)

    def generate_autoscan(self, dataset_id: str) -> str:
        if not self.model: return "AI Offline."
        try:
            summary = eda_engine.generate_summary(dataset_id)
            context = json.dumps(summary, indent=2)
            prompt = f"""
            Act as a Data Analyst. Analyze this summary:
            {context}
            
            1. **Executive Brief**: 2 sentences on data health.
            2. **Key Insight**: 1 major pattern.
            3. **Recommendations**: Generate 3 SHORT, SIMPLE questions for a non-technical user to visualize data.
               - Focus on: Bar Charts, Pie Charts, Line Charts.
               - Format: Just the question text.
            
            **CRITICAL:** Return the questions as a simple JSON list of strings. 
            Example: <QUESTIONS>["Show a bar chart of Pclass", "Show a pie chart of Sex", "Compare Age vs Fare"]</QUESTIONS>
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Autoscan failed: {str(e)}"

    def generate_insight(self, dataset_id: str, query: str = None) -> str:
        if not self.model: return "AI Offline."
        
        query_lower = query.lower()
        
        # --- SIMPLE ML TRIGGER ---
        is_direct_command = ("predict" in query_lower or "train" in query_lower) and \
                            not ("how" in query_lower or "strategy" in query_lower)

        if is_direct_command:
            try:
                summary = eda_engine.generate_summary(dataset_id)
                cols = summary['column_names']
                target_col = next((c for c in cols if c.lower() in query_lower), None)
                if target_col:
                    ml_result = ml_engine.train_model(dataset_id, target_col)
                    if "error" in ml_result: return f"⚠️ {ml_result['error']}"
                    return f"### 🔮 ML Results\n\nI trained a **{ml_result['model_type']}** to predict **{ml_result['target']}**.\n\n**Accuracy:** {ml_result['score']}%\n\n**Top Factors:**\n" + "\n".join([f"- {k}: {v}" for k,v in ml_result['top_features'].items()])
            except Exception as e:
                return f"ML Tool Error: {str(e)}"

        # --- VISUALIZATION FLOW ---
        try:
            # LOAD FULL DATA (Limit to 2000 rows to stay fast)
            df = data_engine.load_data(dataset_id)
            # Convert to dictionary, handling NaNs
            chart_data = df.head(2000).fillna("null").to_dict(orient='records')
            
            history = self.memory_store.get(dataset_id, [])
            history_text = "\n".join([f"{m['role'].upper()}: {m['text']}" for m in history[-5:]])

            full_prompt = f"""
            You are a Data Visualization Expert.
            
            USER QUERY: 
            {query}
            
            FULL RAW DATA (Use this to calculate accurate counts):
            {json.dumps(chart_data)}
            
            INSTRUCTIONS:
            1. **THOUGHT**: <THOUGHT>Plan logic.</THOUGHT>
            2. **CODE**: <CODE>Python code.</CODE>
            3. **ANSWER**: Concise explanation (Max 50 words).
            4. **CHART**: If user asks for a plot, return JSON in <CHART> tags.
            
            **STRICT CHART JSON FORMAT (Chart.js):**
            <CHART>
            {{
                "type": "bar",
                "data": {{
                    "labels": ["Label A", "Label B"],
                    "datasets": [
                        {{
                            "label": "Metric",
                            "data": [10, 20],
                            "backgroundColor": ["#3b82f6", "#60a5fa"]
                        }}
                    ]
                }},
                "options": {{ "responsive": true, "maintainAspectRatio": false }}
            }}
            </CHART>
            """
            
            response = self.model.generate_content(full_prompt)
            answer = response.text
            
            if dataset_id not in self.memory_store: self.memory_store[dataset_id] = []
            self.memory_store[dataset_id].append({"role": "user", "text": query})
            self.memory_store[dataset_id].append({"role": "ai", "text": answer})
            self._save_history()
            
            return answer

        except Exception as e:
            return f"Error: {str(e)}"

ai_engine = AIEngine()
