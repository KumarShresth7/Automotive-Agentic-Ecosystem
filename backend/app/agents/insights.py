from backend.app.graph.state import AgentState
from backend.app.config import llm
from backend.app.tools.vector_store import search_rca_docs
from langchain_core.prompts import ChatPromptTemplate

def insights_agent(state: AgentState):
    """RAG: Retrieves docs and uses Gemini to generate insights."""
    print("--- 🏭 Generating Manufacturing Insights (RAG) ---")
    
    if not state.get("booking_confirmation"):
        return state
        
    diagnosis = state['diagnosis_result']
    component = diagnosis.probable_component
    
    # 1. Retrieve relevant docs from Vector DB
    docs = search_rca_docs(component)
    context_text = "\n\n".join([d.page_content for d in docs])
    
    # 2. Synthesize Insight using LLM
    prompt = ChatPromptTemplate.from_template(
        """
        You are a Manufacturing Quality Engineer.
        A field failure occurred for: {component}.
        
        Here are historical RCA documents retrieved from the database:
        {context}
        
        Based on this, generate a concise technical alert (max 1 sentence) 
        linking this new failure to past patterns.
        """
    )
    
    chain = prompt | llm
    res = chain.invoke({"component": component, "context": context_text})
    
    state['manufacturing_insight'] = res.content
    print(f"Insight Generated: {res.content}")
    
    return state