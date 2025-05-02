import copy
import random
import math

def get_all_possible_moves(board):
    """获取所有合法移动（返回格式优化）"""
    moves = []
    # 行方向扫描
    for i in range(4):
        j = 0
        while j < 4:
            if board[i][j] == 1:
                start = j
                while j < 4 and board[i][j] == 1:
                    j += 1
                end = j - 1
                for s in range(start, end+1):
                    for e in range(s, end+1):
                        moves.append( ('r', i, s, e) )
            else:
                j += 1
    # 列方向扫描
    for j in range(4):
        i = 0
        while i < 4:
            if board[i][j] == 1:
                start = i
                while i < 4 and board[i][j] == 1:
                    i += 1
                end = i - 1
                for s in range(start, end+1):
                    for e in range(s, end+1):
                        moves.append( ('c', j, s, e) )
            else:
                i += 1
    return moves

def apply_move(board, move):
    """应用移动到棋盘"""
    direction, pos, start, end = move
    if direction == 'r':
        for col in range(start, end+1):
            board[pos][col] = 0
    else:
        for row in range(start, end+1):
            board[row][pos] = 0

def simulate_random_game(board, first_player):
    """模拟随机对局并返回胜利者"""
    current_player = first_player
    sim_board = copy.deepcopy(board)
    while True:
        # 检查是否已无棋子
        if sum(sum(row) for row in sim_board) == 0:
            return current_player  # 当前玩家输
        
        # 获取所有合法移动
        moves = get_all_possible_moves(sim_board)
        if not moves:
            return current_player  # 无合法移动时输
        
        # 随机选择移动
        move = random.choice(moves)
        apply_move(sim_board, move)
        
        # 切换玩家
        current_player = 1 - current_player

def monte_carlo_choose_move(board, simulations=100000):
    """蒙特卡洛决策"""
    moves = get_all_possible_moves(board)
    if not moves:
        return None
    
    move_stats = {}
    for move in moves:
        move_stats[move] = {'wins': 0, 'sims': 0}
    
    # 并行评估所有移动
    for _ in range(simulations):
        # 随机选择一个移动进行快速评估
        move = random.choice(moves)
        
        # 创建模拟棋盘
        sim_board = copy.deepcopy(board)
        apply_move(sim_board, move)
        
        # 模拟对局（从对方玩家开始）
        winner = simulate_random_game(sim_board, first_player=0)  # 机器是玩家1
        
        # 更新统计
        move_stats[move]['sims'] += 1
        if winner == 1:  # 机器获胜
            move_stats[move]['wins'] += 1
    
    # 选择胜率最高的移动
    best_move = None
    best_score = -1
    for move, stats in move_stats.items():
        if stats['sims'] == 0:
            continue
        score = stats['wins'] / (stats['sims']+1) 
        if score > best_score:
            best_score = score
            best_move = move
    print(best_score)
    return best_move


# 初始化棋盘和玩家
board = [[1 for _ in range(4)] for _ in range(4)]
players = ['Human', 'Machine']
current_player = 0  # 0: 人类先手

while True:
    print(f"\n{players[current_player]}'s turn:")
    print("Current board (rows 1-4, columns 1-4):")
    for i, row in enumerate(board):
        print(f"{i+1} {' '.join(['X' if cell else '.' for cell in row])}")
    print("  1 2 3 4")

    # 游戏结束检查
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"{players[current_player]} took the last piece and loses!")
        break

    # 人类玩家输入
    if current_player == 0:
        # ...（人类输入部分与之前相同，此处省略以节省篇幅）
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
        move = monte_carlo_choose_move(board)
        direction, pos, start, end = move
        
        # 应用移动
        apply_move(board, move)
        
        # 转换坐标显示
        if direction == 'r':
            start_coord = [pos+1, start+1]
            end_coord = [pos+1, end+1]
        else:
            start_coord = [start+1, pos+1]
            end_coord = [end+1, pos+1]
        
        print(f"Machine's move: From {start_coord} to {end_coord}")

    # 检查游戏结束
    total_pieces = sum(sum(row) for row in board)
    if total_pieces == 0:
        print(f"\n{players[current_player]} took the last piece and loses!")
        break

    # 切换玩家
    current_player = 1 - current_player
