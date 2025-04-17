from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from models import MeetingResponse, db
from fuzzywuzzy import process
from . import dashboard_bp

# Initialize the LLM and conversation
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

@dashboard_bp.route('/response', methods=['GET'])
def view_responses():
    responses = MeetingResponse.query.order_by(MeetingResponse.timestamp.desc()).all()
    return render_template('response.html', responses=responses)

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

    # Handle /help command dynamically from the prompt
    if user_input.strip().lower() == "/help":
        help_text = extract_help_from_prompt(prompt)
        return jsonify({'ai_response': help_text})

    # Normal AI processing
    ai_query = f"{user_input}\n{prompt}\nExtract the following details:\n{template_questions}"
    response = conversation.predict(input=ai_query)

    formatted_response = format_meeting_details(response)

    new_entry = MeetingResponse(user_input=user_input, ai_response=formatted_response)
    db.session.add(new_entry)
    db.session.commit()

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