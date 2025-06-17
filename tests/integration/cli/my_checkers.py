import sys

BOARD_SIZE = 8

def create_board():
    board = []
    for row in range(BOARD_SIZE):
        board_row = []
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                if row < 3:
                    board_row.append('b')  # Black piece
                elif row > 4:
                    board_row.append('w')  # White piece
                else:
                    board_row.append('.')
            else:
                board_row.append(' ')
        board.append(board_row)
    return board

def print_board(board):
    print("    " + " ".join(str(i) for i in range(BOARD_SIZE)))
    print("   " + "--" * BOARD_SIZE)
    for idx, row in enumerate(board):
        print(f"{idx} | " + " ".join(row))
    print()

def is_valid_move(board, player, from_row, from_col, to_row, to_col):
    if not (0 <= from_row < BOARD_SIZE and 0 <= from_col < BOARD_SIZE and
            0 <= to_row < BOARD_SIZE and 0 <= to_col < BOARD_SIZE):
        return False
    piece = board[from_row][from_col]
    dest = board[to_row][to_col]
    if piece.lower() != player or dest != '.':
        return False
    direction = 1 if player == 'b' else -1
    # Normal move
    if abs(to_row - from_row) == 1 and abs(to_col - from_col) == 1:
        if (piece.islower() and (to_row - from_row) == direction) or piece.isupper():
            return True
    # Capture move
    if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        mid_piece = board[mid_row][mid_col]
        if mid_piece != '.' and mid_piece.lower() != player:
            if (piece.islower() and (to_row - from_row) == 2 * direction) or piece.isupper():
                return True
    return False

def make_move(board, player, from_row, from_col, to_row, to_col):
    piece = board[from_row][from_col]
    board[to_row][to_col] = piece
    board[from_row][from_col] = '.'
    # Check for capture
    if abs(to_row - from_row) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        board[mid_row][mid_col] = '.'
    # King me
    if player == 'b' and to_row == BOARD_SIZE - 1:
        board[to_row][to_col] = 'B'
    if player == 'w' and to_row == 0:
        board[to_row][to_col] = 'W'

def has_moves(board, player):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c].lower() == player:
                for dr in [-2, -1, 1, 2]:
                    for dc in [-2, -1, 1, 2]:
                        nr, nc = r + dr, c + dc
                        if is_valid_move(board, player, r, c, nr, nc):
                            return True
    return False

def main():
    board = create_board()
    players = ['b', 'w']
    turn = 0
    while True:
        print_board(board)
        player = players[turn % 2]
        if not has_moves(board, player):
            print(f"Player {'Black' if player == 'b' else 'White'} has no moves. Game over!")
            print(f"Player {'White' if player == 'b' else 'Black'} wins!")
            break
        print(f"Player {'Black' if player == 'b' else 'White'}'s turn ({player.upper()})")
        try:
            move = input("Enter move as from_row from_col to_row to_col (e.g. 2 1 3 0): ")
            if move.lower() in ['quit', 'exit']:
                print("Game exited.")
                break
            from_row, from_col, to_row, to_col = map(int, move.strip().split())
        except Exception:
            print("Invalid input. Try again.")
            continue
        if is_valid_move(board, player, from_row, from_col, to_row, to_col):
            make_move(board, player, from_row, from_col, to_row, to_col)
            turn += 1
        else:
            print("Invalid