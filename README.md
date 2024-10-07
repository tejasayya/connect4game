# connect4game with AI


![](https://github.com/tejasayya/connect4game/blob/main/assets/Alpha-Beta-pygame.gif)




Steps to run the Game.
```
pip install -r requirements.txt
```
```
git clone https://github.com/tejasayya/connect4game.git
```
```
python alphaBeta_801384760.py
```







This Connect Four game implementation utilizes several algorithms to enable the AI opponent to make strategic moves. 

## Below is an overview of each algorithm used:

## 1. Random Move
**Description:** The simplest algorithm where the AI selects a move at random from the list of valid columns that are not yet full.

**Function:**

```
def get_random_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)
```
Usage:

Provides a baseline AI behavior.
Useful for testing and comparing the effectiveness of more advanced algorithms.


## 2. Minimax Algorithm without Pruning
**Description:** The Minimax algorithm is a recursive or backtracking algorithm used in decision-making and game theory to find the optimal move for a player, assuming that the opponent is also playing optimally.

**Function:**

```
def minimax(board, depth, maximizingPlayer):
    # Base case: check for terminal state or depth limit
    if depth == 0 or is_terminal_node(board):
        return (None, score_position(board, AI_PIECE))
    
    valid_locations = get_valid_locations(board)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # Recurse
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            # Recurse
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

```

Usage:

Explores all possible moves up to a certain depth.
Evaluates the board using a heuristic function (score_position).
Chooses the move that maximizes the AI's minimum guaranteed score.


Limitations:
Computationally intensive for larger depths due to exponential growth of possible game states.
Does not incorporate any optimization techniques.


## 3. Alpha-Beta Pruning
**Description:** An optimization of the Minimax algorithm that reduces the number of nodes evaluated in the search tree by pruning branches that cannot possibly affect the final decision.

**Function:**

```
def alpha_beta_search(board, depth, alpha, beta, maximizingPlayer):
    # Base case: check for terminal state or depth limit
    if depth == 0 or is_terminal_node(board):
        return (None, score_position(board, AI_PIECE))
    
    valid_locations = get_valid_locations(board)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # Recurse with updated alpha
            new_score = alpha_beta_search(b_copy, depth - 1, alpha, beta, False)[1]
            value = max(value, new_score)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return col, value
    else:
        value = math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            # Recurse with updated beta
            new_score = alpha_beta_search(b_copy, depth - 1, alpha, beta, True)[1]
            value = min(value, new_score)
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return col, value

```


Usage:

Improves upon Minimax by eliminating branches that won't be chosen.
Uses two parameters, alpha and beta, to keep track of the minimum score that the maximizing player is assured and the maximum score that the minimizing player is assured, respectively.
Significantly reduces the computation time compared to the standard Minimax.


## 4. Alpha-Beta Pruning with Cutoff (Depth Limit)

**Description:** An extension of the Alpha-Beta Pruning algorithm that includes a cutoff depth to limit how deep the algorithm searches the game tree. This is essential for managing computational resources and ensuring the AI makes timely decisions.

**Function:**

```
def alpha_beta_cutoff_search(board, depth, alpha, beta, maximizingPlayer, cutoff):
    # Base case: check for terminal state or cutoff depth
    if depth >= cutoff or is_terminal_node(board):
        return (None, score_position(board, AI_PIECE))
    
    valid_locations = get_valid_locations(board)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # Recurse with increased depth
            new_score = alpha_beta_cutoff_search(b_copy, depth + 1, alpha, beta, False, cutoff)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            # Simulate the move
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            # Recurse with increased depth
            new_score = alpha_beta_cutoff_search(b_copy, depth + 1, alpha, beta, True, cutoff)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return best_col, value

```

Usage:

- Controls the depth of the search tree to prevent excessive computation time.
- Balances between optimal play and practical response time.
- The cutoff parameter allows adjustment of the depth limit based on the desired difficulty and performance constraints.



## Supporting Functions and Concepts
### Evaluation Function (score_position)
- Purpose: Provides a heuristic evaluation of the board from the AI's perspective.
- Method: Scores the board based on potential winning lines, favoring positions that lead to a win and blocking the opponent's opportunities.
- Factors Considered:
  - Center column preference.
  - Horizontal, vertical, and diagonal lines.
  - Number of connected pieces.

### Terminal States (is_terminal_node)
- Purpose: Checks if the game has reached a terminal state (win or draw).
- Usage: Determines when to stop recursion in the Minimax and Alpha-Beta algorithms.

### Valid Moves (get_valid_locations)
- Purpose: Generates a list of columns where a new piece can be placed.
- Usage: Used in all algorithms to determine possible moves.


## AI Algorithm Selection in the Game
The game allows players to select the AI algorithm through UI buttons:

- Random Move
- Minimax
- Alpha-Beta
- Alpha-Beta Cutoff

Depending on the selection, the AI will use the corresponding algorithm to decide its moves. This feature enables players to experience different levels of AI difficulty and observe the impact of various algorithms on gameplay.



