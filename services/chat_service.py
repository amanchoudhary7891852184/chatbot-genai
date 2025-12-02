import os
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from services.vector_store import get_vector_store, add_texts_to_vector_store

# Local LLM Setup
model_id = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    temperature=0.7,  # Increased for more creativity
    top_p=0.95,
    repetition_penalty=1.15
)

local_llm = HuggingFacePipeline(pipeline=pipe)

# Custom Prompt Template
template = """You are a helpful and friendly AI assistant named Dotsy.
You are talking to a user. Use the following context (including chat history) to answer the question.
If the answer is not in the context, just answer from your own knowledge, but be helpful.
Do not say "Show thinking". Be conversational.

Context:
{context}

Chat History:
{history}

User: {question}
Assistant:"""

PROMPT = PromptTemplate(template=template, input_variables=["context", "history", "question"])

def get_chat_response(query: str, history: list):
    vector_store = get_vector_store()
    
    # Get relevant documents from vector store
    context = ""
    if vector_store:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in docs])
    
    # Format history
    history_str = ""
    for msg in history:
        role = "User" if msg.role == "user" else "Assistant"
        history_str += f"{role}: {msg.content}\n"
    
    # Create Chain
    chain = LLMChain(llm=local_llm, prompt=PROMPT)
    
    try:
        response = chain.run(context=context, history=history_str, question=query)
        
        # Save interaction to vector store for long-term memory
        # We save the user query and the assistant response as separate or combined chunks
        # Here we save them combined to keep context
        interaction = f"User: {query}\nAssistant: {response}"
        add_texts_to_vector_store([interaction], metadatas=[{"type": "chat_history"}])
        
    except Exception as e:
        return f"Error generating response: {str(e)}"
        
    return response
