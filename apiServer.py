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
    msg = json.loads(request.data)   
    try:
        jsonschema.validate(instance=msg, schema=querySchema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'error': 'msg is invalid'}) 
    sessionId = msg.setdefault("sessionId", "")
    sessionId = msg["sessionId"]
    if not sessionId:
        sessionId = uuid.uuid4()
    query = msg["query"]    
    return jsonify({'sessionId': sessionId, 'text': query})

@app.route('/api/feedback', methods=['POST'])
def feedback():
    msg = json.loads(request.data)   
    try:
        jsonschema.validate(instance=msg, schema=sessionFeedbackSchema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'error': 'msg is invalid'}) 
    sessionId = msg["sessionId"]
    feedback = msg["feedback"]   
    comments = feedback.setdefault("comments", "") 
    return jsonify({'sessionId': sessionId, 'rating': feedback["rating"], 'comments': comments})


app.run()