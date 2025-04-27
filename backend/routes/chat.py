from fastapi import APIRouter, Request, HTTPException, Depends
from langchain_cohere import CohereEmbeddings, ChatCohere
import psycopg2
import os
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

workflow = StateGraph(state_schema=MessagesState)

# Load environment variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Define the router
router = APIRouter()

# Define the number of similar results to retrieve
top_n = 5

# Initialize the Cohere model with error handling
try:
    model = ChatCohere(temperature=0)
except Exception as e:
    print(f"Error initializing Cohere model: {e}")
    raise HTTPException(
        status_code=500,
        detail="Failed to initialize chat model. Please try again later."
    )

# Create a prompt template for the model
prompt = PromptTemplate.from_template(
    "As a knowledgeable assistant, provide a clear and helpful answer to the user's question."
    "Question: {question}"
    "Context : {context}"
    "Respond concisely and directly:"
)

def call_model(state: MessagesState):
    try:
        system_prompt = (
            "You are a helpful assistant. "
            "Answer all questions to the best of your ability. "
        )
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model.invoke(messages)
        return {"messages": response}
    except Exception as e:
        print(f"Error calling model: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response. Please try again."
        )

workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Function to reset memory and app
def initialize_app():
    global memory, app
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

# Initial setup
initialize_app()

@router.post("")
@limiter.limit("20/minute")
async def chat(request: Request):
    try:
        # Parse incoming JSON data
        data = await request.json()
        message = data.get("message")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Initialize embeddings
        embeddings = CohereEmbeddings(model="embed-english-v3.0")
        
        # Connect to the database with connection pooling
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                try:
                    query_embedding = embeddings.embed_query(message)

                    # Check if the query embedding is empty
                    if not query_embedding:
                        raise HTTPException(
                            status_code=400,
                            detail="Could not process your question. Please try rephrasing it."
                        )

                    # Check if the embeddings table exists
                    cur.execute(
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM information_schema.tables
                            WHERE table_name = 'embeddings'
                        );
                        """
                    )

                    if not cur.fetchone()[0]:
                        raise HTTPException(
                            status_code=404,
                            detail="No documents found. Please upload a document first."
                        )

                    # Perform semantic search
                    cur.execute(
                        """
                        SELECT text, embedding, 1 - (embedding <=> %s::vector) AS similarity
                        FROM embeddings
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                        """,
                        (query_embedding, query_embedding, top_n),
                    )

                    # Fetch and return the results
                    results = cur.fetchall()

                    if not results:
                        raise HTTPException(
                            status_code=404,
                            detail="No relevant information found in the documents."
                        )

                    context_data = [{"text": result[0]} for result in results]

                except psycopg2.Error as e:
                    print(f"Database error: {e}")
                    raise HTTPException(
                        status_code=500,
                        detail="Database error occurred. Please try again later."
                    )

        context = context_data[0]["text"] if context_data else ""

        try:
            final = app.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=prompt.invoke(
                                {"question": message, "context": context}
                            ).to_string()
                        )
                    ]
                },
                config={"configurable": {"thread_id": "1"}},
            )

            return final.get("messages")[len(final.get("messages")) - 1].content

        except Exception as e:
            print(f"Error generating response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response. Please try again."
            )

    except RateLimitExceeded:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait before trying again."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

# The below function clears the memory
@router.get("/clear")
@limiter.limit("10/minute")
async def clear(request: Request):
    try:
        initialize_app()  # Reinitialize memory and app
        return {"message": "Memory cleared successfully"}
    except Exception as e:
        print(f"Error clearing memory: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to clear memory. Please try again."
        )
