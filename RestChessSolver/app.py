



from flask import Flask, request, abort
import Rest_chess_solver
import json
import sys

chess_solver = Rest_chess_solver.GameOfChess()
app = Flask(__name__)


@app.route("/api/v1/check/<current_field>", methods=["GET", "POST"])
def check(current_field):
    if request.method == "POST" or request.method == "GET":
        chess_solver.list_available_moves(current_field)
        with open("avaliable_moves.json", "r") as f:
            data = json.load(f)

        match data["error"]:
            case "There is no figure on field chosen by you.":
                return abort(404, data)
            case "none":
                return data


@app.route("/api/v1/<current_field>/<dest_field>", methods=["GET", "POST"])
def index(current_field, dest_field):
    if request.method == "POST" or request.method == "GET":

        chess_solver.move(current_field, dest_field)
        with open("answer.json", "r") as f:
            data = json.load(f)

        match data["error"]:
            case "there is no figure on field, field is empty":
                return abort(404, data)
            case "none":
                return data
            case "Current move is not permitted.":
                return abort(409, data)


if __name__ == "__main__":
    selectedport = 0
    if len(sys.argv) > 1:
        selectedport = sys.argv[1]
    if selectedport:
        app.run(debug=True, port=sys.argv[1])
    else:
        app.run(debug=True)