from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class GameBoard:
    def __init__(self):
        self.board: Board = [
            [Color.NONE if i == j else Color.UNCOLORED for j in range(NUM_NODES)]
            for i in range(NUM_NODES)
        ]

    def color_edge(self, edge: Edge, color: Color) -> None:
        a, b = edge
        self.board[a][b] = color
        self.board[b][a] = color

    def get_winner(self) -> Color | None:
        for i in range(NUM_NODES):
            for j in range(i + 1, NUM_NODES):
                c = self.board[i][j]
                if c != Color.P1 and c != Color.P2:
                    continue
                for k in range(j + 1, NUM_NODES):
                    if self.board[i][k] == c and self.board[j][k] == c:
                        return Color.P2 if c == Color.P1 else Color.P1
        return None

    def __str__(self):
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string