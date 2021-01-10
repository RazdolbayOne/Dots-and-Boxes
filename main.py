# Author: aqeelanwar
# Created: 13 March,2020, 9:19 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np

BOARD_SIZE = 600
BLANK_SPACE=150# space where will be buttons
NUMBER_OF_DOTS_ON_BOARD = 2
SYMBOL_SIZE = (BOARD_SIZE / 3 - BOARD_SIZE / 8) / 2
SYMBOL_THICKNESS = 50
DOT_COLOR = '#7BC043'
PLAYER1_COLOR = '#0492CF'
PLAYER1_COLOR_LIGHT = '#67B0CF'
PLAYER2_COLOR = '#EE4035'
PLAYER2_COLOR_LIGHT = '#EE7E77'
GREEN_COLOR = '#7BC043'
DOT_WIDTH = 0.25 * BOARD_SIZE / NUMBER_OF_DOTS_ON_BOARD
EDGE_WIDTH = 0.1 * BOARD_SIZE / NUMBER_OF_DOTS_ON_BOARD
DISTANCE_BETWEEN_DOTS = BOARD_SIZE / (NUMBER_OF_DOTS_ON_BOARD)


class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self, is_first_player_starts):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=BOARD_SIZE+BLANK_SPACE, height=BOARD_SIZE)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = is_first_player_starts
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(NUMBER_OF_DOTS_ON_BOARD - 1, NUMBER_OF_DOTS_ON_BOARD - 1))
        self.row_status = np.zeros(shape=(NUMBER_OF_DOTS_ON_BOARD, NUMBER_OF_DOTS_ON_BOARD - 1))
        self.col_status = np.zeros(shape=(NUMBER_OF_DOTS_ON_BOARD - 1, NUMBER_OF_DOTS_ON_BOARD))

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - DISTANCE_BETWEEN_DOTS / 4) // (DISTANCE_BETWEEN_DOTS / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = PLAYER1_COLOR_LIGHT
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = PLAYER2_COLOR_LIGHT
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val = - 1

        if c < (NUMBER_OF_DOTS_ON_BOARD - 1) and r < (NUMBER_OF_DOTS_ON_BOARD - 1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r - 1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = DISTANCE_BETWEEN_DOTS / 2 + logical_position[0] * DISTANCE_BETWEEN_DOTS
            end_x = start_x + DISTANCE_BETWEEN_DOTS
            start_y = DISTANCE_BETWEEN_DOTS / 2 + logical_position[1] * DISTANCE_BETWEEN_DOTS
            end_y = start_y
        elif type == 'col':
            start_y = DISTANCE_BETWEEN_DOTS / 2 + logical_position[1] * DISTANCE_BETWEEN_DOTS
            end_y = start_y + DISTANCE_BETWEEN_DOTS
            start_x = DISTANCE_BETWEEN_DOTS / 2 + logical_position[0] * DISTANCE_BETWEEN_DOTS
            end_x = start_x

        if self.player1_turn:
            color = PLAYER1_COLOR
        else:
            color = PLAYER2_COLOR
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=EDGE_WIDTH)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = PLAYER1_COLOR
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = PLAYER2_COLOR
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(BOARD_SIZE / 2, BOARD_SIZE / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(BOARD_SIZE / 2, 5 * BOARD_SIZE / 8, font="cmr 40 bold", fill=GREEN_COLOR,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(BOARD_SIZE / 2, 3 * BOARD_SIZE / 4, font="cmr 30 bold", fill=GREEN_COLOR,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(BOARD_SIZE / 2, 15 * BOARD_SIZE / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(NUMBER_OF_DOTS_ON_BOARD):
            x = i * DISTANCE_BETWEEN_DOTS + DISTANCE_BETWEEN_DOTS / 2
            self.canvas.create_line(x, DISTANCE_BETWEEN_DOTS / 2, x,
                                    BOARD_SIZE - DISTANCE_BETWEEN_DOTS / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(DISTANCE_BETWEEN_DOTS / 2, x,
                                    BOARD_SIZE - DISTANCE_BETWEEN_DOTS / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(NUMBER_OF_DOTS_ON_BOARD):
            for j in range(NUMBER_OF_DOTS_ON_BOARD):
                start_x = i * DISTANCE_BETWEEN_DOTS + DISTANCE_BETWEEN_DOTS / 2
                end_x = j * DISTANCE_BETWEEN_DOTS + DISTANCE_BETWEEN_DOTS / 2
                self.canvas.create_oval(start_x - DOT_WIDTH / 2, end_x - DOT_WIDTH / 2, start_x + DOT_WIDTH / 2,
                                        end_x + DOT_WIDTH / 2, fill=DOT_COLOR,
                                        outline=DOT_COLOR)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = PLAYER1_COLOR
        else:
            text += 'Player2'
            color = PLAYER2_COLOR

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(BOARD_SIZE - 5 * len(text),
                                                       BOARD_SIZE - DISTANCE_BETWEEN_DOTS / 8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def shade_box(self, box, color):
        start_x = DISTANCE_BETWEEN_DOTS / 2 + box[1] * DISTANCE_BETWEEN_DOTS + EDGE_WIDTH / 2
        start_y = DISTANCE_BETWEEN_DOTS / 2 + box[0] * DISTANCE_BETWEEN_DOTS + EDGE_WIDTH / 2
        end_x = start_x + DISTANCE_BETWEEN_DOTS - EDGE_WIDTH
        end_y = start_y + DISTANCE_BETWEEN_DOTS - EDGE_WIDTH
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Dots_and_Boxes(True)
game_instance.mainloop()
