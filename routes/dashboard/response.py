from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3, os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from models import MeetingResponse
from fuzzywuzzy import process
from . import dashboard_bp
from dotenv import load_dotenv
from extension import db
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#from routes.dashboard.pinecone_store import add_to_vector_db


load_dotenv()

# Initialize the LLM and conversation
#llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(temperature=0,model_name="llama3-70b-8192",openai_api_base="https://api.groq.com/openai/v1",openai_api_key=os.getenv("GROQ_API_KEY"))
#llm = ChatOpenAI(model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",openai_api_key=os.getenv("TOGETHER_API_KEY"),openai_api_base="https://api.together.xyz/v1",temperature=0.7)

memory = ConversationBufferMemory(k=5)
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)


@dashboard_bp.route('/response', methods=['GET'])
def view_responses():
    responses = MeetingResponse.query.order_by(MeetingResponse.timestamp.desc()).all()
    return render_template('dashboard/response.html', responses=responses)

@dashboard_bp.route('/process-text', methods=['POST'])
def process_text():
    user_input = request.form.get('text')
    prompt_id = request.form.get('prompt_id')

    if not user_input or not prompt_id:
        return jsonify({'error': 'No text or prompt ID provided'}), 400

    # Fetch the full prompt
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT prompt, template_file FROM autogpt1 WHERE id = ?", (prompt_id,))
        row = cur.fetchone()

    if not row:
        return jsonify({'error': 'Prompt not found'}), 400

    prompt = row["prompt"]
    template_questions = row["template_file"]
    #input_expected = row["input_expected"]

    # Handle /help command dynamically from the prompt
    if user_input.strip().lower() == "/help":
        help_text = extract_help_from_prompt(prompt)
        return jsonify({'ai_response': help_text})

    # Normal AI processing
    ai_query = f"{user_input}\n{prompt}\nExtract the following details:\n{template_questions}"

    memory.clear()

    response = conversation.predict(input=ai_query)
   
    formatted_response = format_meeting_details(response)

    new_entry = MeetingResponse(user_input=user_input, ai_response=formatted_response)
    db.session.add(new_entry)
    db.session.commit()

    # Store vector in Pinecone with metadata
    #add_to_vector_db(formatted_response, metadata={"prompt_id": prompt_id, "user_input": user_input})

    return jsonify({'ai_response': formatted_response})
    

 
def extract_help_from_prompt(prompt_text):
    lines = prompt_text.strip().split("\n")
    
    # Try to find the start of numbered instructions
    for i, line in enumerate(lines):
        if line.strip().startswith("10."):
            # Return the paragraph(s) before that as the help message
            return "\n".join(lines[:i]).strip()

    # Fallback: just return the first 10 lines
    return "\n".join(lines[:10]).strip()

def format_meeting_details(text):
    """Formats the extracted text into a structured, line-by-line format."""
    lines = text.split("\n")
    formatted_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(formatted_lines)


#from routes.dashboard.pinecone_store import search_similar

#@dashboard_bp.route('/search-vector', methods=['POST'])
#def search_vector():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    results = search_similar(query)
    return jsonify({
        "results": [
            {"text": r.page_content, "metadata": r.metadata} for r in results
        ]
    })





