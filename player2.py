from __future__ import annotations
from itertools import combinations

from consts import Board, Color, Edge, NUM_NODES


class Player2:
    @staticmethod
    def get_move(board: Board) -> Edge:
        mini = Player2.get_miniboard(board)
        if mini is None:
            raise ValueError("No miniboard with a P2-allowed move exists")

        candidates = Player2.get_allowed_moves(Color.P2, mini)
        if len(candidates) == 1:
            return candidates[0]

        p2_sets = Player2.get_maximal_allowed_sets(Color.P2, mini)
        candidates = Player2._keep_most_frequent(candidates, p2_sets)
        if len(candidates) == 1:
            return candidates[0]

        p1_sets = Player2.get_maximal_allowed_sets(Color.P1, mini)
        candidates = Player2._keep_most_frequent(candidates, p1_sets)
        return candidates[0]

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        exists = [
            any(board[i][j] != Color.NONE for j in range(NUM_NODES))
            for i in range(NUM_NODES)
        ]
        required = []
        free = []
        for i in range(NUM_NODES):
            if not exists[i]:
                continue
            touched = any(
                board[i][j] == Color.P1 or board[i][j] == Color.P2
                for j in range(NUM_NODES)
            )
            (required if touched else free).append(i)

        for k in range(len(free) + 1):
            for extra in combinations(free, k):
                keep = set(required) | set(extra)
                mini = Player2._restrict(board, keep)
                if Player2.get_allowed_moves(Color.P2, mini):
                    return mini
        return None

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        moves = Player2.get_allowed_moves(player, board)
        n = len(moves)

        adj = [set() for _ in range(NUM_NODES)]
        for i in range(NUM_NODES):
            for j in range(NUM_NODES):
                if board[i][j] == player:
                    adj[i].add(j)

        best = 0
        results: set[frozenset[Edge]] = set()
        chosen: list[Edge] = []

        def dfs(i: int) -> None:
            nonlocal best, results
            if len(chosen) + (n - i) < best:
                return
            if i == n:
                if len(chosen) > best:
                    best = len(chosen)
                    results = set()
                results.add(frozenset(chosen))
                return
            a, b = moves[i]
            if not (adj[a] & adj[b]):
                adj[a].add(b)
                adj[b].add(a)
                chosen.append((a, b))
                dfs(i + 1)
                chosen.pop()
                adj[a].discard(b)
                adj[b].discard(a)
            dfs(i + 1)

        dfs(0)
        return results

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        moves: list[Edge] = []
        for i in range(NUM_NODES):
            for j in range(i + 1, NUM_NODES):
                if board[i][j] != Color.UNCOLORED:
                    continue
                if any(
                    board[i][k] == player and board[j][k] == player
                    for k in range(NUM_NODES)
                ):
                    continue
                moves.append((i, j))
        return moves

    @staticmethod
    def _restrict(board: Board, keep: set[int]) -> Board:
        mini = [row[:] for row in board]
        for i in range(NUM_NODES):
            if i in keep:
                continue
            for j in range(NUM_NODES):
                mini[i][j] = Color.NONE
                mini[j][i] = Color.NONE
        return mini

    @staticmethod
    def _keep_most_frequent(
        moves: list[Edge], sets: set[frozenset[Edge]]
    ) -> list[Edge]:
        counts = [sum(1 for s in sets if move in s) for move in moves]
        top = max(counts)
        return [m for m, c in zip(moves, counts) if c == top]