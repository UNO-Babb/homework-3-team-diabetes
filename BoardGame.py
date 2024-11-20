from flask import Flask, render_template, redirect, url_for, request
import random
import json

app = Flask(__name__)

app.jinja_env.globals.update(enumerate=enumerate)

# File to save and load game state
SAVE_FILE = "sorry_game_state.json"

# Default board and game state
def default_game_state():
    return {
        "players": {
            "Player 1": {"position": 0, "home": False},
            "Player 2": {"position": 0, "home": False},
        },
        "turn": "Player 1",
        "board": ["Start"] + ["Space " + str(i) for i in range(1, 20)] + ["Home"],
        "cards": ["Move 1", "Move 2", "Move 3", "Move 4", "Move 5", "Sorry!"],
    }

# Save the game state
def save_game_state(game_state):
    with open(SAVE_FILE, "w") as f:
        json.dump(game_state, f)

# Load the game state
def load_game_state():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default_game_state()

@app.route("/")
def index():
    game_state = load_game_state()
    return render_template("sorry_index.html", game_state=game_state)

@app.route("/draw_card")
def draw_card():
    game_state = load_game_state()
    current_player = game_state["turn"]
    other_player = "Player 2" if current_player == "Player 1" else "Player 1"
    
    card = random.choice(game_state["cards"])

    # Process the card
    if "Move" in card:
        move = int(card.split()[-1])
        game_state["players"][current_player]["position"] += move
        if game_state["players"][current_player]["position"] >= len(game_state["board"]):
            game_state["players"][current_player]["home"] = True
    elif card == "Sorry!":
        # Send the other player back to start
        game_state["players"][other_player]["position"] = 0

    # Switch turn
    game_state["turn"] = other_player

    save_game_state(game_state)
    return redirect(url_for("index"))

@app.route("/reset")
def reset_game():
    save_game_state(default_game_state())
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
