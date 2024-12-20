# %% [markdown]
# Constants and global variables 

# %%
POSITION_PLACEHOLDER = '_'
PLAYER_1 = 1
PLAYER_2 = 2
CROSS_CHAR = 'X'
CIRCLE_CHAR = 'O'

WINNING_COMBINATIONS = [
  (0, 1, 2),  # Top row
  (3, 4, 5),  # Middle row
  (6, 7, 8),  # Bottom row
  (0, 3, 6),  # Left column
  (1, 4, 7),  # Middle column
  (2, 5, 8),  # Right column
  (0, 4, 8),  # Diagonal from top-left to bottom-right
  (2, 4, 6)   # Diagonal from top-right to bottom-left
]


# %% [markdown]
# Util

# %%
def player_desc(active_player):
  return 'Player One (1)' if active_player == PLAYER_1 else 'Player Two (2)'

# %% [markdown]
# Init

# %%
def init_board(board):
  board = [POSITION_PLACEHOLDER] * 9
  return board

# %% [markdown]
# Display board

# %%
def display(board):
  print('-XOX- TIC-TAC-TOE in Python -XOX-')
  print()
  print('-------------')

  for row in range(3):
    print('|', end='')
    for col in range(3):
      print(f' {board[row * 3 + col]} |', end='')
    print()

  print('-------------')


# %% [markdown]
# Ask for user input

# %%
def user_turn(board, active_player):
  position = -1

  while position not in range(1,10):
    position_input = input(f'{player_desc(active_player)} choose position (1-9): ')
    
    if position_input.isdigit():
      position = int(position_input)
    
    if position not in range(1,10):
      print('Please choose a valid position')
    elif board[position - 1] != POSITION_PLACEHOLDER:
      print('Please choose an empty position')
      position = -1

  return position

# %% [markdown]
# Update position

# %%
def update_position(board, position, active_player):
  if active_player == PLAYER_1:
    board[position - 1] = CROSS_CHAR
    return PLAYER_2
  else:
    board[position - 1] = CIRCLE_CHAR
    return PLAYER_1

# %% [markdown]
# Switch active player

# %%
def switch_active_player(active_player):
  if active_player == PLAYER_1:
    return PLAYER_2
  else:
    return PLAYER_1

# %% [markdown]
# Check winner

# %%
def check_win_status(board):
  for combo in WINNING_COMBINATIONS:
    if board[combo[0]] == board[combo[1]] == board[combo[2]] != POSITION_PLACEHOLDER:
      return True

  return False

# %% [markdown]
# Run game

# %%
from IPython.display import clear_output

def run_game():
  board = init_board([])
  display(board)

  game_on = True
  turns_played = 0
  active_player = PLAYER_1

  while game_on:
    position = user_turn(board, active_player)
    
    active_player = update_position(board, position, active_player)
    
    clear_output()
    display(board)

    if check_win_status(board):
      winner = 'ONE' if active_player == PLAYER_2 else 'TWO'
      print()
      print(f'PLAYER {winner} WINS!')
      game_on = False

    turns_played += 1

    if turns_played == 9:
      print('TIE GAME')
      game_on = False
  

# %%
run_game()
