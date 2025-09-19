# Hotel Query Agent

An LLM-powered agent that queries hotel data using LangGraph orchestration and Streamlit interface.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variable**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
   
   Or on Windows:
   ```cmd
   set OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **Prepare Dataset**
   - Ensure `hotels.csv` is in the same directory as `app.py`
   - The sample CSV provided includes all required columns

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Features

- 🏨 **Hotel Search**: Query hotels by city, country, ratings, and amenities
- 🔧 **LangGraph Integration**: Orchestrated agent workflow with tool use
- 💬 **Chat Interface**: Natural language queries in a conversational format
- 📊 **Structured Results**: Clear tabular display of hotel information
- 🎯 **Smart Filtering**: Support for multiple criteria and sorting options

## Example Queries

- "Top 5 hotels in Paris by cleanliness"
- "Hotels in Japan with at least 4 stars"
- "Best comfort hotels in New York"
- "Show me 3 hotels in London sorted by facilities"
- "Hotels with cleanliness above 8.5 in Italy"

## Architecture

- **LangGraph**: Orchestrates the agent workflow with tool calling
- **Streamlit**: Provides the chat interface
- **Custom Tool**: Single `query_hotels` tool for dataset queries
- **Data Management**: Normalized CSV loading with proper error handling

## Dataset Requirements

The CSV must contain these columns:
- `hotel_id`: Unique identifier
- `hotel_name`: Hotel name
- `city`: City name
- `country`: Country name
- `lat`: Latitude
- `lon`: Longitude
- `star_rating`: Star rating (0-5)
- `cleanliness_base`: Cleanliness score
- `comfort_base`: Comfort score
- `facilities_base`: Facilities score