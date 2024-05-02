from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def handle_post_request():
    # Your handling logic here
    data = request.json  # Access the JSON data sent in the request
    # Process the data as needed
    if len(data['messages']) > 1:
        print("$ - Flask Server = ", data['messages'])
        return jsonify({"messages": "Received POST request, here is the data = " + data['messages']})
    else:
        print("$ - Flask Server = Received OPTIONS request")
        return jsonify({"messages": "Received OPTIONS request"})

if __name__ == "__main__": 
    from waitress import serve
    print("$ - hello from server")
    serve(app, host='0.0.0.0', port=8080)
