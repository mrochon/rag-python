import json
import jsonschema
import uuid

# User query schema
querySchema = {
    "type": "object",
    "properties": {
        "sessionId": {"type": "string"},
        "query": {"type": "string"},
    },
    "required": ["query"],
}
sessionFeedbackSchema = {
    "type": "object",
    "properties": {
        "sessionId": {"type": "string"},
        "feedback": {
            "type": "object",
            "properties": {
                "rating": {"type": "number"},
                "comments": {"type": "string"},
            },
            "required": ["rating"]
        }
    },
    "required": ["sessionId", "feedback"],
}
from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 415
    #msg = json.loads(request.data)   
    try:
        msg = request.get_json()
        jsonschema.validate(instance=msg, schema=querySchema)
    except Exception as e:
        return jsonify({'error': 'msg is invalid'}), 400
    sessionId = msg.setdefault("sessionId", "")
    sessionId = msg["sessionId"]
    if not sessionId:
        sessionId = uuid.uuid4()
    query = msg["query"]  
    # If existing session for this user (authn needs ading), read history from db otherwise create new guid for session
    # Create new prompt
    # Call completions API
    # Save query, completion, tokens used to history
    # return response 
    answer = f"This is a response to your query: {query}" 
    return jsonify({'sessionId': sessionId, 'answer': answer})

@app.route('/api/feedback', methods=['POST'])
def feedback():
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 415
    try:
        msg = json.loads(request.data) 
        jsonschema.validate(instance=msg, schema=sessionFeedbackSchema)
    except Exception as e:
        return jsonify({'error': 'msg is invalid'}), 400
    sessionId = msg["sessionId"]
    feedback = msg["feedback"]   
    comments = feedback.setdefault("comments", "") 
    # Save feedback to history
    return jsonify({'sessionId': sessionId, 'rating': feedback["rating"], 'comments': comments})

app.run()