import random

def get_all_possible_moves(board):
    """获取所有合法移动"""
    moves = []
    # 检查所有行
    for i in range(4):
        row = board[i]
        j = 0
        while j < 4:
            if row[j] == 1:
                start = j
                while j < 4 and row[j] == 1:
                    j += 1
                end = j - 1
                # 生成所有可能的连续子区间
                for s in range(start, end + 1):
                    for e in range(s, end + 1):
                        moves.append(('r', i, s, e))
            else:
                j += 1
    # 检查所有列
    for j in range(4):
        col = [board[i][j] for i in range(4)]
        i = 0
        while i < 4:
            if col[i] == 1:
                start_row = i
                while i < 4 and col[i] == 1:
                    i += 1
                end_row = i - 1
                # 生成所有可能的连续子区间
                for s in range(start_row, end_row + 1):
                    for e in range(s, end_row + 1):
                        moves.append(('c', j, s, e))
            else:
                i += 1
    return moves

def machine_choose_move(board):
    """机器随机选择一个合法移动"""
    moves = get_all_possible_moves(board)
    if not moves:
        return None  # 无合法移动（理论上不会发生）
    return random.choice(moves)

# 初始化棋盘和玩家
board = [[1 for _ in range(4)] for _ in range(4)]
players = ['Human', 'Machine']
current_player = 0  # 0: Human先手，1: Machine后手

while True:
    print(f"\n{players[current_player]}'s turn:")
    print("Current board (rows 1-4, columns 1-4):")
    for i, row in enumerate(board):
        print(f"{i+1} {' '.join(['X' if cell else '.' for cell in row])}")
    print("   1 2 3 4")

    # 检查棋盘是否为空（游戏结束）
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"{players[current_player]} took the last piece and loses!")
        break

    # 人类玩家输入或机器自动选择
    if current_player == 0:  # 人类玩家
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

                    # 检查所选位置是否有棋子
                    valid = all(board[row][col] == 1 for col in range(start_col, end_col + 1))
                    if not valid:
                        print("Selected positions must be consecutive and have pieces (X).")
                        continue

                    # 更新棋盘
                    for col in range(start_col, end_col + 1):
                        board[row][col] = 0
                    break

                else:  # 列操作
                    col = int(input("Enter column number (1-4): ")) - 1
                    if col < 0 or col >= 4:
                        print("Column number must be between 1 and 4.")
                        continue

                    start_row = int(input("Enter start row (1-4): ")) - 1
                    end_row = int(input("Enter end row (1-4): ")) - 1
                    if start_row < 0 or start_row >= 4 or end_row < 0 or end_row >= 4 or start_row > end_row:
                        print("Invalid row range.")
                        continue

                    # 检查所选位置是否有棋子
                    valid = all(board[row][col] == 1 for row in range(start_row, end_row + 1))
                    if not valid:
                        print("Selected positions must be consecutive and have pieces (X).")
                        continue

                    # 更新棋盘
                    for row in range(start_row, end_row + 1):
                        board[row][col] = 0
                    break

            except ValueError:
                print("Invalid input. Please enter numbers only.")
    else:  # 机器玩家
        print("Machine is thinking...")
        move = machine_choose_move(board)
        direction, pos, start, end = move
        if direction == 'r':
            row = pos
            start_col = start
            end_col = end
            for col in range(start_col, end_col + 1):
                board[row][col] = 0
            start_coord = [row + 1, start_col + 1]
            end_coord = [row + 1, end_col + 1]
        else:
            col = pos
            start_row = start
            end_row = end
            for row in range(start_row, end_row + 1):
                board[row][col] = 0
            start_coord = [start_row + 1, col + 1]
            end_coord = [end_row + 1, col + 1]
        print(f"Machine's move: from {start_coord} to {end_coord}")

    # 检查棋盘是否为空
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"\n{players[current_player]} took the last piece and loses!")
        break

    # 切换玩家
    current_player = 1 - current_player