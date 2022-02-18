



import json
from chess import parse_square, PIECE_NAMES, \
    RANK_NAMES, FILE_NAMES, Move, Board

# comment added as


class GameOfChess:
    last_move = ""
    figure_name = ""
    Exceptions = ""
    emptyfield_flag = False

    answerdict = {
        "move": "invalid",
        "figure": "rook",
        "error": "",
        "currentField": "H2",
        "destField": "H3",
    }

    av_mov_res = {
        "availableMoves": ["a1b2"],
        "figure": "rook",
        "error": "Current move is not permitted.",
        "currentField": "H2",
    }
    board = 0

    def __init__(self):
        self.board = Board()

    def get_legal_move(self):
        return self.board.legal_moves

    def get_figure_name_at_field(self, current_position):
        try:
            f_ind = parse_square(str(current_position))
            figure_name = PIECE_NAMES[self.board.piece_type_at(f_ind)]
            self.emptyfield_flag = False
        except Exception as e:
            print("field is empty")
            figure_name = "empty_field"
            self.emptyfield_flag = True
            self.Exceptions = e.__class__

        return figure_name

    def printboard(self):
        print(self.board)

    def check_possible_moves(self, field):
        p_mov = []
        for name in FILE_NAMES:
            for number in RANK_NAMES:
                if (name + number) != field:
                    move = Move.from_uci(field + name + number)
                    if move in self.board.legal_moves:
                        p_mov.append(field+"->"+name + number)
        return p_mov

    def get_last_move(self):
        return self.last_move

    def list_available_moves(self, field_to_check):

        list_of_avaliable_moves = self.check_possible_moves(field_to_check)

        if list_of_avaliable_moves:
            self.av_mov_res["availableMoves"] = list_of_avaliable_moves
            self.av_mov_res["figure"] = self.get_figure_name_at_field(
                field_to_check
            )
            self.av_mov_res["currentField"] = field_to_check
            if self.emptyfield_flag:
                self.av_mov_res[
                    "error"
                ] = "There is no figure on field chosen by you."
            else:
                self.av_mov_res["error"] = "none"
        else:
            self.av_mov_res["availableMoves"] = "no moves avaliable"
            self.av_mov_res["figure"] = self.get_figure_name_at_field(
                field_to_check
            )
            self.av_mov_res["currentField"] = field_to_check
            if self.emptyfield_flag:
                self.av_mov_res[
                    "error"
                ] = "There is no figure on field chosen by you."
            else:
                self.av_mov_res["error"] = "none"
        with open("avaliable_moves.json", "w") as json_file:
            json.dump(self.av_mov_res, json_file)
        return self.av_mov_res

    def move(self, movefrom, moveto):
        figure_to_move = self.get_figure_name_at_field(movefrom)
        match self.emptyfield_flag:
            case False:
                move = Move.from_uci(movefrom + moveto)
                self.last_move = movefrom + moveto

                if move in self.board.legal_moves:
                    self.answerdict["figure"] = figure_to_move
                    self.answerdict["move"] = "valid"
                    self.answerdict["error"] = "none"
                    self.answerdict["destField"] = moveto
                    self.answerdict["currentField"] = movefrom
                    self.board.push(move)  # Make the move
                    print("valid move")

                else:
                    self.answerdict["figure"] = figure_to_move
                    self.answerdict["move"] = "invalid"
                    self.answerdict["error"] = "Current move is not permitted."
                    self.answerdict["destField"] = moveto
                    self.answerdict["currentField"] = movefrom
                    print("illegal move")

            case True:
                self.answerdict["figure"] = figure_to_move
                self.answerdict["move"] = "invalid"
                self.answerdict["error"] = "there is no figure on field,\
                     field is empty"
                self.answerdict["destField"] = moveto
                self.answerdict["currentField"] = movefrom
                print("there is no figure on chosen field, field is empty")

        self.printboard()
        with open("answer.json", "w") as json_file:
            json.dump(self.answerdict, json_file)