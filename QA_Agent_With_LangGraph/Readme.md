# 🏨 Hotel Query Agent

An interactive Streamlit application powered by **LangGraph** that lets you explore hotels from a structured dataset (`hotels.csv`).  
Ask natural-language questions like:

- *“Top 5 hotels in Paris by cleanliness”*  
- *“Show me hotels in Spain with at least 4 stars and high comfort ratings”*  

The app will query the dataset, apply filters, and return results in a **tabular text summary**.

---

## ✨ Features

- Loads `hotels.csv` once per session and normalizes columns for consistent filtering.  
- Single **query tool** supporting:
  - City and country filters (case-insensitive).  
  - Minimum thresholds for star rating, cleanliness, comfort, and facilities.  
  - Sorting by star rating, cleanliness, comfort, or facilities.  
  - Clamped result limits `[1–10]`.  
- LangGraph agent ensures the LLM always uses the tool when asked data-related questions.  
- Streamlit chat UI with natural-language queries and conversational responses.  
- Graceful handling of empty results with alternative query suggestions.

---

## 📂 Dataset Requirements

The `hotels.csv` must contain the following columns:

- `hotel id`  
- `hotel name`  
- `city`  
- `country`  
- `lat`  
- `lon`  
- `star rating`  
- `cleanliness base`  
- `comfort base`  
- `facilities base`  

⚠️ Ensure column names match exactly (case-insensitive check will normalize them).  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/roshan5619/hotel-query-agent.git
cd hotel-query-agent
```
2. Install dependencies

We recommend using a virtual environment.
```
pip install -r requirements.txt
```
3. Set up environment variables

Create a .env file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here

```
4. Prepare dataset

Place hotels.csv in the project root.

5. Run the app
```
streamlit run app.py
```
