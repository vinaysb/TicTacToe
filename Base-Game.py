import numpy as np
import pygame as pg


class TicTacToe:
    def __init__(self):
        pg.init()
        self.board = np.zeros((3, 3))

        self.done = False
        self.cell_vals = []
        self.DISPLAY_WIDTH = 300
        self.DISPLAY_HEIGHT = 300
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (26, 219, 39)
        self.RED = (255, 0, 0)
        self.GREY = (105, 105, 105)
        self.screen = pg.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pg.display.set_caption('Tic-Tac-Toe')
        self.clock = pg.time.Clock()

        self.Clickable_Areas = {
            1: pg.Rect(10, 10, 90, 90),
            2: pg.Rect(110, 10, 90, 90),
            3: pg.Rect(210, 10, 90, 90),
            4: pg.Rect(10, 110, 90, 90),
            5: pg.Rect(110, 110, 90, 90),
            6: pg.Rect(210, 110, 90, 90),
            7: pg.Rect(10, 210, 90, 90),
            8: pg.Rect(110, 210, 90, 90),
            9: pg.Rect(210, 210, 90, 90),
            }
        self.Cross = pg.transform.scale(pg.image.load('Cross.png'), (80, 80))
        self.Circle = pg.transform.scale(pg.image.load('Circle.png'), (80, 80))
        self.pos_mapping = {
            1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
            }
        self.rev_pos_mapping = {
            (0, 0): 1, (0, 1): 2, (0, 2): 3, (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9
            }
        self.char_mapping = {0: ' ', 1: 'X', 2: 'O'}
        self.img_mapping = {1: self.Cross, 2: self.Circle}
        self.font = pg.font.Font('Roboto-Regular.ttf', 45)
        self.result = 0

        self.controller()

    def controller(self):
        while not np.all(self.board) and not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                self.screen.fill(self.WHITE)
                pg.draw.line(self.screen, self.BLACK, [100, 10], [100, 290], 5)
                pg.draw.line(self.screen, self.BLACK, [200, 10], [200, 290], 5)
                pg.draw.line(self.screen, self.BLACK, [10, 100], [290, 100], 5)
                pg.draw.line(self.screen, self.BLACK, [10, 200], [290, 200], 5)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for area in self.Clickable_Areas:
                            if self.Clickable_Areas[area].collidepoint(pg.mouse.get_pos()):
                                self.cell_vals.append((area, 1))
                                self.player_turn(area)
                                if np.all(self.board) or self.done:
                                    break
                                self.cell_vals.append((self.computer_turn(), 2))
                                break
            if not self.cell_vals == []:
                for area, val in self.cell_vals:
                    self.screen.blit(self.img_mapping[val], self.Clickable_Areas[area])
            if np.all(self.board):
                self.result = 3
            if self.result:
                result_mapping = {1: ('You Won!!', self.GREEN),
                                  2: ('You Lost!!', self.RED),
                                  3: ('It was a Draw!!', self.GREY)}
                self.screen.fill(self.WHITE)
                textsurf = self.font.render(result_mapping[self.result][0], True, result_mapping[self.result][1])
                textrect = textsurf.get_rect()
                textrect.center = (150, 150)
                self.screen.blit(textsurf, textrect)
                pg.display.update()
                pg.time.delay(1000)
            pg.display.update()
            self.clock.tick(60)
        pg.quit()

    def _win_cond(self, board, pos):
        x, y = self.pos_mapping[pos]
        if board[(0, y)] == board[(1, y)] and board[(0, y)] == board[(2, y)]:
            return True
        elif board[(x, 0)] == board[(x, 1)] and board[(x, 0)] == board[(x, 2)]:
            return True
        if pos in [1, 5, 9]:
            if board[(0, 0)] == board[(1, 1)] and board[(0, 0)] == board[(2, 2)]:
                return True
        if pos in [3, 5, 7]:
            if board[(0, 2)] == board[(1, 1)] and board[(0, 2)] == board[(2, 0)]:
                return True
        return False

    def player_turn(self, x):
        self.board[self.pos_mapping[x]] = 1
        if self._win_cond(np.copy(self.board), x):
            self.done = True
            self.result = 1

    def computer_turn(self):
        empty_pos = list(zip(*np.where(self.board == 0)))
        pos_decided = False
        # Move for comp to win
        for zero_pos in empty_pos:
            pos = self.rev_pos_mapping[zero_pos]
            board = np.copy(self.board)
            board[zero_pos] = 2
            if self._win_cond(board, pos):
                x = pos
                pos_decided = True
                break
        # Move to stop player from winning
        if not pos_decided:
            for zero_pos in empty_pos:
                pos = self.rev_pos_mapping[zero_pos]
                board = np.copy(self.board)
                board[zero_pos] = 1
                if self._win_cond(board, pos):
                    x = pos
                    pos_decided = True
                    break
        # Check if corners are empty and select that if it is
        if not pos_decided:
            for zero_pos in empty_pos:
                pos = self.rev_pos_mapping[zero_pos]
                if pos in [1, 3, 7, 9]:
                    x = pos
                    pos_decided = True
                    break
        # Check if center is empty and select that if it is
        if not pos_decided:
            for zero_pos in empty_pos:
                pos = self.rev_pos_mapping[zero_pos]
                if pos == 5:
                    x = pos
                    pos_decided = True
                    break
        # Select the side is nothing else worked
        if not pos_decided:
            for zero_pos in empty_pos:
                pos = self.rev_pos_mapping[zero_pos]
                if pos in [2, 4, 6, 8]:
                    x = pos
                    pos_decided = True
                    break
        self.board[self.pos_mapping[x]] = 2
        if self._win_cond(np.copy(self.board), x):
            self.done = True
            self.result = 2
        return x


T = TicTacToe()
