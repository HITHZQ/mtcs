import tkinter as tk
from tkinter import messagebox
import copy
import random
import math
import threading

# ---------------------------- 原有游戏逻辑（稍作修改） ----------------------------
def get_all_possible_moves(board):
    """生成所有合法移动"""
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
                        if all(board[i][col] == 1 for col in range(s, e+1)):
                            moves.append(('r', i, s, e))
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
                        if all(board[row][j] == 1 for row in range(s, e+1)):
                            moves.append(('c', j, s, e))
            else:
                i += 1
    return moves

def apply_move(board, move):
    """应用移动"""
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

def monte_carlo_choose_move(board, total_sims=10000, exploration_param=1.2):
    """基于UCT算法的优化蒙特卡洛决策"""
    moves = get_all_possible_moves(board)
    if not moves:
        return None

    move_stats = {move: {'wins': 0, 'sims': 0} for move in moves}
    total_sims_done = 0

    # 初始阶段：为每个移动分配至少一次模拟
    for move in moves:
        sim_board = copy.deepcopy(board)
        apply_move(sim_board, move)
        winner = simulate_random_game(sim_board, first_player=0)
        move_stats[move]['sims'] += 1
        total_sims_done += 1
        if winner == 1:
            move_stats[move]['wins'] += 1

    # 动态分配剩余模拟次数
    for _ in range(total_sims - len(moves)):
        max_uct = -float('inf')
        best_move = None

        # 计算每个移动的UCT值
        for move, stats in move_stats.items():
            if stats['sims'] == 0:
                uct = float('inf')  # 强制探索未模拟的移动（理论上不会发生）
            else:
                exploitation = stats['wins'] / stats['sims']
                exploration = exploration_param * math.sqrt(math.log(total_sims_done) / stats['sims'])
                uct = exploitation + exploration

            if uct > max_uct:
                max_uct = uct
                best_move = move
        

        # 模拟最佳移动
        sim_board = copy.deepcopy(board)
        apply_move(sim_board, best_move)
        winner = simulate_random_game(sim_board, first_player=0)
        move_stats[best_move]['sims'] += 1
        total_sims_done += 1
        if winner == 1:
            move_stats[best_move]['wins'] += 1
    print((max_uct))
    # 选择胜率最高的移动
    best_move = max(move_stats.items(),
                    key=lambda x: (x[1]['wins'] / x[1]['sims']) if x[1]['sims'] > 0 else 0)
    return best_move[0]


# 初始化棋盘和玩家
board = [[1 for _ in range(4)] for _ in range(4)]
players = ['Human', 'Machine']
current_player = 0  # 0: 人类先手


# ---------------------------- GUI界面 ----------------------------
class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("策略棋盘游戏")
        self.board = [[1 for _ in range(4)] for _ in range(4)]
        self.current_player = 0  # 0:人类 1:机器
        self.selection_mode = None  # 当前选择模式：None/'row'/'col'
        self.selection_start = None
        
        # 界面组件
        self.create_widgets()
        self.update_board()
        
        # 如果机器先手
        if self.current_player == 1:
            self.machine_move()
    
    def create_widgets(self):
        """创建界面组件"""
        # 棋盘网格
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.root, width=4, height=2,
                              command=lambda i=i, j=j: self.on_cell_click(i, j))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.cells.append(row)
        
        # 控制面板
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=4, columnspan=4, pady=10)
        
        self.status_label = tk.Label(control_frame, text="玩家回合", font=('Arial', 12))
        self.status_label.pack()
        
        self.row_btn = tk.Button(control_frame, text="选择行", command=self.select_row_mode)
        self.row_btn.pack(side=tk.LEFT, padx=5)
        
        self.col_btn = tk.Button(control_frame, text="选择列", command=self.select_col_mode)
        self.col_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="重新开始", command=self.reset_game)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_board(self):
        """更新棋盘显示"""
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 1:
                    self.cells[i][j].config(bg='gold', relief=tk.RAISED)
                else:
                    self.cells[i][j].config(bg='gray', relief=tk.SUNKEN)
    
    def select_row_mode(self):
        """进入行选择模式"""
        self.selection_mode = 'row'
        self.selection_start = None
        self.status_label.config(text="请选择起始位置")
    
    def select_col_mode(self):
        """进入列选择模式"""
        self.selection_mode = 'col'
        self.selection_start = None
        self.status_label.config(text="请选择起始位置")
    
    def on_cell_click(self, i, j):
        """优化后的点击事件处理"""
        if self.current_player != 0 or not self.selection_mode:
            return

    # 第一阶段：选择行/列
        if self.selection_mode in ['row', 'col'] and self.selection_start is None:
        # 验证选择有效性
            if (self.selection_mode == 'row' and self.board[i][j] == 1) or \
           (self.selection_mode == 'col' and self.board[i][j] == 1):  # 修正坐标映射
                self.selection_start = (i, j)
                self.status_label.config(text="请选择结束位置" if self.selection_mode == 'row' else "请选择结束位置")
                self.cells[i][j].config(relief=tk.SUNKEN)  # 视觉反馈
            else:
                self.status_label.config(text="请选择有棋子的位置！")
            return

    # 第二阶段：选择范围
        try:
            if self.selection_mode == 'row':
            # 确保在同一行操作
                if i != self.selection_start[0]:
                    raise ValueError("必须选择同一行")
            
            # 获取列范围
                start_col = min(self.selection_start[1], j)
                end_col = max(self.selection_start[1], j)
            
            # 验证连续性
                if not all(self.board[i][col] == 1 for col in range(start_col, end_col+1)):
                    raise ValueError("所选范围必须连续且包含棋子")
            
            # 应用移动
                apply_move(self.board, ('r', i, start_col, end_col))
            
            elif self.selection_mode == 'col':
            # 确保在同一列操作
                if j != self.selection_start[1]:
                    raise ValueError("必须选择同一列")
            
            # 获取行范围
                start_row = min(self.selection_start[0], i)
                end_row = max(self.selection_start[0], i)
            
            # 验证连续性
                if not all(self.board[row][j] == 1 for row in range(start_row, end_row+1)):
                    raise ValueError("所选范围必须连续且包含棋子")
            
            # 应用移动
                apply_move(self.board, ('c', j, start_row, end_row))
        
        # 重置选择状态
            self.selection_mode = None
            self.selection_start = None
            self.update_board()
            self.check_game_over()
        
        # 切换玩家
            self.current_player = 1
            self.machine_move()

        except Exception as e:
            self.status_label.config(text=str(e))
        # 重置选择并刷新界面
            self.selection_start = None
            self.selection_mode = None
            self.update_board()

# 新增视觉反馈方法
    def highlight_range(self, start, end, direction):
        """高亮显示选择范围"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(relief=tk.RAISED)
    
        if direction == 'r':
            row = start[0]
            for col in range(start[1], end[1]+1):
                self.cells[row][col].config(relief=tk.SUNKEN)
        else:
            col = start[1]
            for row in range(start[0], end[0]+1):
                self.cells[row][col].config(relief=tk.SUNKEN)
    
    def machine_move(self):
        """机器移动（使用线程防止界面冻结）"""
        def threaded_move():
            self.status_label.config(text="机器正在思考...")
            move = monte_carlo_choose_move(self.board)
            apply_move(self.board, move)
            
            self.root.after(0, lambda: [
                self.update_board(),
                self.check_game_over(),
                setattr(self, 'current_player', 0),
                self.status_label.config(text="玩家回合")
            ])
        
        threading.Thread(target=threaded_move).start()
    
    def check_game_over(self):
        """检查游戏是否结束"""
        if sum(sum(row) for row in self.board) == 0:
            loser = "人类" if self.current_player == 0 else "机器"
            messagebox.showinfo("游戏结束", f"{loser}拿走了最后一个棋子，游戏结束！")
            self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        self.board = [[1 for _ in range(4)] for _ in range(4)]
        self.current_player = 0
        self.selection_mode = None
        self.update_board()
        self.status_label.config(text="玩家回合")
    
    def run(self):
        self.root.mainloop()

# ---------------------------- 启动游戏 ----------------------------
if __name__ == "__main__":
    game = GameGUI()
    game.run()