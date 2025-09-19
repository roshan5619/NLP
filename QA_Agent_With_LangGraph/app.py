import streamlit as st
import pandas as pd
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import json

# Configuration
st.set_page_config(page_title="Hotel Query Agent", page_icon="🏨", layout="wide")

@dataclass
class HotelQueryParams:
    """Parameters for hotel queries"""
    city: Optional[str] = None
    country: Optional[str] = None
    min_star_rating: float = 0.0
    min_cleanliness: float = 0.0
    min_comfort: float = 0.0
    min_facilities: float = 0.0
    sort_by: str = "star_rating"
    limit: int = 5

class HotelDataManager:
    """Manages hotel dataset loading and querying"""
    
    def __init__(self):
        self.df = None
        self.required_columns = [
            'hotel_id', 'hotel_name', 'city', 'country', 
            'lat', 'lon', 'star_rating', 'cleanliness_base', 
            'comfort_base', 'facilities_base'
        ]
    
    def load_data(self, file_path: str = "hotels.csv") -> bool:
        """Load and normalize the hotel dataset"""
        try:
            self.df = pd.read_csv(file_path)
            
            # Check for required columns
            missing_cols = [col for col in self.required_columns if col not in self.df.columns]
            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
                return False
            
            # Normalize data
            self.df['city'] = self.df['city'].str.strip().str.lower()
            self.df['country'] = self.df['country'].str.strip().str.lower()
            
            # Ensure numeric columns are properly typed
            numeric_cols = ['star_rating', 'cleanliness_base', 'comfort_base', 'facilities_base']
            for col in numeric_cols:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # Remove rows with missing critical data
            self.df = self.df.dropna(subset=numeric_cols)
            
            return True
            
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return False
    
    def query_hotels(self, params: HotelQueryParams) -> Dict[str, Any]:
        """Query hotels based on parameters"""
        if self.df is None:
            return {"error": "Dataset not loaded"}
        
        # Start with all data
        filtered_df = self.df.copy()
        
        # Apply filters
        if params.city:
            city_filter = params.city.strip().lower()
            filtered_df = filtered_df[filtered_df['city'].str.contains(city_filter, na=False)]
        
        if params.country:
            country_filter = params.country.strip().lower()
            filtered_df = filtered_df[filtered_df['country'].str.contains(country_filter, na=False)]
        
        # Apply minimum thresholds
        filtered_df = filtered_df[
            (filtered_df['star_rating'] >= params.min_star_rating) &
            (filtered_df['cleanliness_base'] >= params.min_cleanliness) &
            (filtered_df['comfort_base'] >= params.min_comfort) &
            (filtered_df['facilities_base'] >= params.min_facilities)
        ]
        
        if filtered_df.empty:
            return {
                "results": [],
                "total_found": 0,
                "message": "No hotels found matching your criteria."
            }
        
        # Sort results
        valid_sort_columns = ['star_rating', 'cleanliness_base', 'comfort_base', 'facilities_base']
        if params.sort_by in valid_sort_columns:
            filtered_df = filtered_df.sort_values(params.sort_by, ascending=False)
        
        # Limit results (clamp between 1 and 10)
        limit = max(1, min(10, params.limit))
        result_df = filtered_df.head(limit)
        
        # Format results
        results = []
        for _, row in result_df.iterrows():
            results.append({
                "hotel_name": row['hotel_name'],
                "city": row['city'].title(),
                "country": row['country'].title(),
                "star_rating": float(row['star_rating']),
                "cleanliness": float(row['cleanliness_base']),
                "comfort": float(row['comfort_base']),
                "facilities": float(row['facilities_base'])
            })
        
        return {
            "results": results,
            "total_found": len(filtered_df),
            "message": f"Found {len(filtered_df)} hotel(s), showing top {len(results)}"
        }

# Initialize hotel data manager
@st.cache_resource
def get_hotel_manager():
    manager = HotelDataManager()
    if manager.load_data():
        return manager
    return None

# Define the tool
hotel_manager = get_hotel_manager()

@tool
def query_hotels(
    city: Optional[str] = None,
    country: Optional[str] = None,
    min_star_rating: float = 0.0,
    min_cleanliness: float = 0.0,
    min_comfort: float = 0.0,
    min_facilities: float = 0.0,
    sort_by: str = "star_rating",
    limit: int = 5
) -> str:
    """
    Query hotels from the dataset based on specified criteria.
    
    Args:
        city: City to filter by (case-insensitive)
        country: Country to filter by (case-insensitive)
        min_star_rating: Minimum star rating (0-5)
        min_cleanliness: Minimum cleanliness score
        min_comfort: Minimum comfort score
        min_facilities: Minimum facilities score
        sort_by: Column to sort by (star_rating, cleanliness_base, comfort_base, facilities_base)
        limit: Maximum number of results to return (1-10)
    
    Returns:
        JSON string with query results
    """
    if hotel_manager is None:
        return json.dumps({"error": "Hotel dataset not available"})
    
    params = HotelQueryParams(
        city=city,
        country=country,
        min_star_rating=min_star_rating,
        min_cleanliness=min_cleanliness,
        min_comfort=min_comfort,
        min_facilities=min_facilities,
        sort_by=sort_by,
        limit=limit
    )
    
    result = hotel_manager.query_hotels(params)
    return json.dumps(result)

# LangGraph Agent Setup
def create_agent():
    """Create the LangGraph agent"""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set the OPENAI_API_KEY environment variable")
        return None
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools([query_hotels])
    
    # System prompt
    system_prompt = """You are a helpful hotel search assistant. When users ask about hotels, you should:

1. Use the query_hotels tool to search the hotel database
2. Always provide results in a clear, tabular text format
3. Include hotel name, location, star rating, and key scores (cleanliness, comfort, facilities)
4. If no results are found, suggest alternative searches (e.g., broader criteria, different cities)
5. Be conversational and helpful in your responses

The tool accepts these parameters:
- city, country: for location filtering (case-insensitive)
- min_star_rating, min_cleanliness, min_comfort, min_facilities: for quality filtering
- sort_by: choose from 'star_rating', 'cleanliness_base', 'comfort_base', 'facilities_base'
- limit: number of results (1-10)

Always use the tool when users ask about hotels, even for general questions about hotel data."""
    
    def agent_node(state: MessagesState):
        messages = state["messages"]
        # Add system message if not present
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def format_response_node(state: MessagesState):
        """Format the final response with hotel data"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the last message has tool calls, don't modify it
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return {"messages": []}
        
        # Check if we have tool responses to format
        tool_results = []
        for msg in reversed(messages):
            if hasattr(msg, 'content') and isinstance(msg.content, str):
                try:
                    # Check if this looks like a tool result
                    if msg.content.startswith('{"results":') or msg.content.startswith('{"error":'):
                        data = json.loads(msg.content)
                        tool_results.append(data)
                        break
                except:
                    continue
        
        if tool_results and 'results' in tool_results[0]:
            data = tool_results[0]
            if data['results']:
                # Format as table
                formatted_response = f"{data['message']}\n\n"
                formatted_response += "📍 **Hotel Results:**\n\n"
                formatted_response += "| Hotel Name | Location | ⭐ Rating | 🧽 Clean | 🛏️ Comfort | 🏢 Facilities |\n"
                formatted_response += "|------------|----------|-----------|----------|------------|---------------|\n"
                
                for hotel in data['results']:
                    formatted_response += f"| {hotel['hotel_name']} | {hotel['city']}, {hotel['country']} | {hotel['star_rating']:.1f} | {hotel['cleanliness']:.1f} | {hotel['comfort']:.1f} | {hotel['facilities']:.1f} |\n"
                
                return {"messages": [AIMessage(content=formatted_response)]}
            else:
                no_results_msg = f"{data['message']}\n\n💡 **Suggestions:**\n- Try searching in a different city\n- Lower your rating requirements\n- Remove some filters"
                return {"messages": [AIMessage(content=no_results_msg)]}
        
        return {"messages": []}
    
    # Create the graph
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode([query_hotels]))
    workflow.add_node("format_response", format_response_node)
    
    # Add edges
    workflow.add_edge("agent", "tools")
    workflow.add_edge("tools", "format_response")
    workflow.add_edge("format_response", "agent")
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    return workflow.compile()

# Streamlit UI
def main():
    st.title("🏨 Hotel Query Agent")
    st.markdown("Ask me about hotels! I can help you find hotels based on location, ratings, and amenities.")
    
    # Check if dataset is loaded
    if hotel_manager is None:
        st.error("❌ Could not load hotels.csv dataset. Please ensure the file exists in the current directory.")
        st.info("The dataset should contain columns: hotel_id, hotel_name, city, country, lat, lon, star_rating, cleanliness_base, comfort_base, facilities_base")
        return
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        st.info("You can set it by running: `export OPENAI_API_KEY=your_api_key_here`")
        return
    
    st.success("✅ Dataset loaded successfully!")
    
    # Create agent
    agent = create_agent()
    if agent is None:
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about hotels (e.g., 'Top 5 hotels in Paris by cleanliness')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Searching hotels..."):
                try:
                    # Invoke agent
                    response = agent.invoke({
                        "messages": [HumanMessage(content=prompt)]
                    })
                    
                    # Get the final response
                    final_message = response["messages"][-1]
                    assistant_response = final_message.content
                    
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Sidebar with example queries
    with st.sidebar:
        st.header("💡 Example Queries")
        example_queries = [
            "Top 5 hotels in Paris by cleanliness",
            "Hotels in Japan with at least 4 stars",
            "Best comfort hotels in New York",
            "Show me 3 hotels in London sorted by facilities",
            "Hotels with cleanliness above 8.5 in Italy"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{query}"):
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()
        
        st.header("ℹ️ Dataset Info")
        if hotel_manager and hotel_manager.df is not None:
            st.write(f"📊 Total hotels: {len(hotel_manager.df)}")
            st.write(f"🌍 Countries: {hotel_manager.df['country'].nunique()}")
            st.write(f"🏙️ Cities: {hotel_manager.df['city'].nunique()}")

if __name__ == "__main__":
    main()