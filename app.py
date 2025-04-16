from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Sample warehouse inventory: { item_name: [quantity, shelf_location] }
inventory = {
    "laptop": [10, "A1"],
    "keyboard": [15, "B2"],
    "mouse": [20, "C3"],
    "monitor": [8, "A2"],
    "tablet": [12, "D1"],
    "printer": [5, "E4"],
    "scanner": [7, "E2"],
    "webcam": [18, "F1"],
    "speaker": [9, "B1"],
    "router": [14, "G3"],
    "headphones": [25, "C4"],
    "microphone": [6, "F2"],
    "hard drive": [11, "H1"],
    "usb cable": [30, "H3"],
    "power adapter": [13, "G1"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_product_info', methods=['POST'])
def get_product_info():
    data = request.get_json()
    user_input = data.get("query", "").lower()

    # Handle Add command: "add 5 tablets to shelf D2"
    match_add = re.search(r"add\s+(\d+)\s+(\w+(?:\s\w+)*)\s+(?:to\s+shelf\s+)?([a-zA-Z0-9]+)", user_input)
    if match_add:
        quantity = int(match_add.group(1))
        item = match_add.group(2).strip()
        location = match_add.group(3).upper()

        if item in inventory:
            inventory[item][0] += quantity
        else:
            inventory[item] = [quantity, location]

        return jsonify({"response": f"Added {quantity} {item}(s) to shelf {location}."})

    # Handle Remove command: "remove the mouse"
    match_remove = re.search(r"(remove|delete)\s+(the\s+)?(\w+(?:\s\w+)*)", user_input)
    if match_remove:
        item = match_remove.group(3).strip()
        if item in inventory:
            del inventory[item]
            return jsonify({"response": f"{item.capitalize()} removed from inventory."})
        else:
            return jsonify({"response": f"{item.capitalize()} not found in inventory."})

    # Handle query command: "what is the stock of laptops?"
    for item in inventory:
        if item in user_input:
            quantity, location = inventory[item]
            return jsonify({"response": f"We have {quantity} {item}s on shelf {location}."})

    return jsonify({"response": "Sorry, I couldn't find information about that product."})

if __name__ == '__main__':
    app.run(debug=True, port=8000)