from flask import Flask, request, jsonify  # Import Flask and the functions you need to handle requests and respond with JSON
import re

app = Flask(__name__)  # Create an instance of the Flask app

data = {  # A dictionary that will act as an in-memory database to store data
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}  

@app.route('/')  # Defines a test route for the root of the application
def home():
    return "Server is running!"  # Returns a simple message to confirm that the server is running

@app.route('/item/<key>', methods=['GET'])  # Defines a route to handle GET requests for a specific item
def get_item(key):
    if key in data:  # Check if the key exists in the dictionary
        return jsonify(data[key])  # Returns the value associated with the key in JSON format
    else:
        return "404, Not Found", 404  # Returns a message, along with the error code to inform the user

@app.route('/list', methods=['GET'])  # Defines a route to handle GET requests for a specific item
def get_list():
    if data:  # Check if the key exists in the dictionary
        array = list(data.keys())
        return jsonify({"Items count": len(array),"All items": array })  # Returns the value associated with the key in JSON format  
    else:
        return "404, Not Found", 404  # Returns a message, along with the error code to inform the user

@app.route('/item', methods=['POST'])  # Defines a route to handle POST requests to create a new item
def post_item():
    x = len(data)  # Stores the number of keys 
    item = request.json  # Gets JSON data from the request
    key = item.get('key')  # Extracts the key from the JSON object
    x += 1  # Adds one key to its length
    value = item.get('value')  # Extracts the value from the JSON object
    y = re.search("[0-9]", value)  # Searches if there is at least one number in the value
    if key in data:  # Check if the key already exists in the dictionary
        return "Item already exists, try deleting some keys before adding new ones", 400  # Returns a message, along with the error code to inform the user
    elif x < 6 and y:  # If there are less than 5 keys and there is a number in the value
        data[key] = value  # Adds the new item to the dictionary
        return jsonify({key: value}), 201  # Returns the newly created item in JSON format with a status code of 201
    elif x > 5 and not y:  # If more than 5 keys are taken and there is no number in the value
        return "Your value must contain at least one number and there can be maximum 5 keys", 202  # Message to inform the user and exit code
    elif not y:  # If there is no number in the value
        return "Your value must contain at least one number.", 202  # Message to inform the user and exit code
    elif x > 5:  # If there are more than 5 keys
        return "There can be maximum 5 keys, try again.", 202  # Message to inform the user and exit code

@app.route('/item/<key>', methods=['PUT'])  # Defines a route to handle PUT requests to create or update a specific item
def put_item(key):
    x = len(data)  # Stores the number of keys 
    x += 1  # Adds one key to its length
    value = request.json.get('value')  # Extracts the value from the JSON object
    y = re.search("[0-9]", value)  # Searches if there is at least one number in the value
    if x < 6 and y:  # If there are less than 5 keys and there is a number in the value
        data[key] = value  # Update or create a new dictionary entry with the specified key
        return jsonify({key: value}), 201  # Returns the newly created item in JSON format with a status code of 201
    elif  x > 5 and not y:  # If more than 5 keys are taken and there is no number in the value
        return "Your value must contain at least one number and there can be maximum 5 keys.", 202  # Message to inform the user and exit code
    elif not y:  # If there is no number in the value
        return "Your value must contain at least one number.", 202  # Message to inform the user and exit code
    elif x > 5:  # If there are more than 5 keys
        return "There can be maximum 5 keys, try again.", 202  # Message to inform the user and exit code

@app.route('/item/<key>', methods=['PATCH'])  # Defines a route to handle PATCH requests to partially update a specific item
def patch_item(key):
    x = len(data)  # Stores the number of keys 
    x += 1  # Adds one key to its length
    if key in data:  # Check if the key already exists in the dictionary
        value = request.json.get('value')  # Extracts the value from the JSON object
        y = re.search("[0-9]", value)  # Searches if there is at least one number in the value
        if y:  # If there is at least one number in the value
            data[key] = value  # Update the value of the existing key in the dictionary
            return jsonify({key: value})  # Returns the updated item in JSON format
        else:
            return "Your value must contain at least one number.", 202  # Message to inform the user and exit code
    elif x > 5:  # If there are more than 5 keys
            return "404, Not Found. Remember that there are maximum 5 keys", 404  # Message to inform the user and exit code
    else:
        return "404, Not Found", 404  # Message to inform the user and exit code

@app.route('/item/<key>', methods=['DELETE'])  # Defines a route to handle DELETE requests to delete a specific item
def delete_item(key):
    if key in data:  # Check if the key exists in the dictionary
        del data[key]  # Delete the entry associated with the key from the dictionary
        return 'Operation successful', 204  # Returns a 204 status code with no content
    else:
        return "404, Not Found", 404  # Message to inform the user and exit code

if __name__ == '__main__':  # Check if the file runs directly and not imported as a module
    app.run(debug=True)  # Start the server in debug mode
