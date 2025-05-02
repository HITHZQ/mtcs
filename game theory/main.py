board = [[1 for _ in range(4)] for _ in range(4)]
players = ['Player 1', 'Player 2']
current_player = 0

while True:
    print(f"\n{players[current_player]}'s turn:")
    print("Current board (rows 1-4, columns 1-4):")
    for i, row in enumerate(board):
        print(f"{i+1} {' '.join(['X' if cell else '.' for cell in row])}")
    print("  1 2 3 4")

    # Check if the board is empty (game over)
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"{players[current_player]} took the last piece and loses!")
        break

    # Get valid move from the current player
    while True:
        direction = input("Enter direction (r for row, c for column): ").strip().lower()
        if direction not in ['r', 'c']:
            print("Invalid direction. Please enter 'r' or 'c'.")
            continue

        try:
            if direction == 'r':
                row = int(input("Enter row number (1-4): ")) - 1
                if row < 0 or row >= 4:
                    print("Row number must be between 1 and 4.")
                    continue

                start_col = int(input("Enter start column (1-4): ")) - 1
                end_col = int(input("Enter end column (1-4): ")) - 1
                if start_col < 0 or start_col >= 4 or end_col < 0 or end_col >= 4 or start_col > end_col:
                    print("Invalid column range.")
                    continue

                # Check if all selected positions have pieces
                valid = all(board[row][col] == 1 for col in range(start_col, end_col + 1))
                if not valid:
                    print("Selected positions must be consecutive and have pieces (X).")
                    continue

                # Update the board
                for col in range(start_col, end_col + 1):
                    board[row][col] = 0
                break

            else:  # direction == 'c'
                col = int(input("Enter column number (1-4): ")) - 1
                if col < 0 or col >= 4:
                    print("Column number must be between 1 and 4.")
                    continue

                start_row = int(input("Enter start row (1-4): ")) - 1
                end_row = int(input("Enter end row (1-4): ")) - 1
                if start_row < 0 or start_row >= 4 or end_row < 0 or end_row >= 4 or start_row > end_row:
                    print("Invalid row range.")
                    continue

                # Check if all selected positions have pieces
                valid = all(board[row][col] == 1 for row in range(start_row, end_row + 1))
                if not valid:
                    print("Selected positions must be consecutive and have pieces (X).")
                    continue

                # Update the board
                for row in range(start_row, end_row + 1):
                    board[row][col] = 0
                break

        except ValueError:
            print("Invalid input. Please enter numbers only.")

    # Check if the board is empty after the move
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"\n{players[current_player]} took the last piece and loses!")
        break

    # Switch to the other player
    current_player = 1 - current_player