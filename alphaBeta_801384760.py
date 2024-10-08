# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2024
# Lab 3
# Adversarial Search / Game Playing
# This module implements "MiniMax", "Alpha-Beta", "Alpha-Beta Cutoff"
# Student ID: 801384760



import numpy as np
import random
import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Define Colors
BLUE = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game Constants
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 80  
RADIUS = int(SQUARESIZE / 2 - 5)

STATUS_BAR_HEIGHT = SQUARESIZE
BOARD_START_Y = STATUS_BAR_HEIGHT
BOARD_HEIGHT = ROW_COUNT * SQUARESIZE
BUTTONS_HEIGHT = int(SQUARESIZE * 1.5)
BUTTONS_START_Y = BOARD_START_Y + BOARD_HEIGHT
LOG_HEIGHT = int(SQUARESIZE * 1.5)
LOG_START_Y = BUTTONS_START_Y + BUTTONS_HEIGHT

width = COLUMN_COUNT * SQUARESIZE
height = LOG_START_Y + LOG_HEIGHT

size = (width, height)
screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("monospace", 60)
smallfont = pygame.font.SysFont("monospace", 20)
logfont = pygame.font.SysFont("monospace", 16)

node_count = 0
log_messages = []

start_button = pygame.Rect(10, BUTTONS_START_Y + 10, 150, 40)
restart_button = pygame.Rect(170, BUTTONS_START_Y + 10, 150, 40)
exit_button = pygame.Rect(330, BUTTONS_START_Y + 10, 150, 40)

algo_buttons = {
    "Random Move": pygame.Rect(10, BUTTONS_START_Y + 60, 100, 40),
    "Minimax": pygame.Rect(120, BUTTONS_START_Y + 60, 100, 40),
    "Alpha-Beta": pygame.Rect(230, BUTTONS_START_Y + 60, 100, 40),
    "A-BCutoff": pygame.Rect(340, BUTTONS_START_Y + 60, 100, 40)
}

selected_algo = "Alpha-Beta"  


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return True

    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return True

    
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return True

   
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

   
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c: c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

   
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r: r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

 
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)


    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (winning_move(board, PLAYER_PIECE) or
            winning_move(board, AI_PIECE) or
            len(get_valid_locations(board)) == 0)


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def draw_board(board):
   
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen, BLUE,
                (c * SQUARESIZE, BOARD_START_Y + r * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            pygame.draw.circle(
                screen, BLACK,
                (int(c * SQUARESIZE + SQUARESIZE / 2),
                 int(BOARD_START_Y + r * SQUARESIZE + SQUARESIZE / 2)),
                RADIUS
            )

   
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen, RED,
                    (int(c * SQUARESIZE + SQUARESIZE / 2),
                     int(BOARD_START_Y + (ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen, YELLOW,
                    (int(c * SQUARESIZE + SQUARESIZE / 2),
                     int(BOARD_START_Y + (ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS
                )

   
    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, WHITE, restart_button)
    pygame.draw.rect(screen, WHITE, exit_button)

    start_label = smallfont.render("New Game", True, BLACK)
    restart_label = smallfont.render("Restart", True, BLACK)
    exit_label = smallfont.render("Exit", True, BLACK)

    screen.blit(start_label, (start_button.x + 10, start_button.y + 5))
    screen.blit(restart_label, (restart_button.x + 20, restart_button.y + 5))
    screen.blit(exit_label, (exit_button.x + 50, exit_button.y + 5))

   
    for algo_name, rect in algo_buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        label = smallfont.render(algo_name, True, BLACK)
        screen.blit(label, (rect.x + 5, rect.y + 5))

   
    pygame.draw.rect(screen, RED, algo_buttons[selected_algo], 3)

  
    pygame.draw.rect(
        screen, BLACK,
        (0, LOG_START_Y, width, LOG_HEIGHT)
    )

    pygame.display.update()


def draw_status(turn):
    pygame.draw.rect(screen, BLACK, (0, 0, width, STATUS_BAR_HEIGHT))
    if turn == PLAYER:
        status = "Player's Turn"
        color = RED
    else:
        status = f"AI's Turn ({selected_algo})"
        color = YELLOW
    label = smallfont.render(status, True, color)
    screen.blit(label, (10, 10))
    pygame.display.update()


def draw_log():
    pygame.draw.rect(screen, BLACK, (0, LOG_START_Y, width, LOG_HEIGHT))
    for i, message in enumerate(log_messages[-3:]):
        label = logfont.render(message, True, WHITE)
        screen.blit(label, (10, LOG_START_Y + i * 30 + 10))
    pygame.display.update()


def show_game_over(winner):
    pygame.draw.rect(
        screen, BLACK,
        (50, height // 2 - 100, width - 100, 200)
    )
    if winner == "Player":
        text = "Player Wins!"
        color = RED
    elif winner == "AI":
        text = "AI Wins!"
        color = YELLOW
    else:
        text = "It's a Draw!"
        color = WHITE
    game_over_font = pygame.font.SysFont("monospace", 60)
    label = game_over_font.render(text, True, color)
    screen.blit(
        label,
        (width // 2 - label.get_width() // 2, height // 2 - label.get_height() // 2)
    )
    pygame.display.update()
    pygame.time.wait(3000)



def get_random_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)



def minimax(board, depth, maximizingPlayer):
    global node_count
    node_count += 1
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else: 
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value



def alpha_beta_search(board, depth, alpha, beta, maximizingPlayer):
    global node_count
    node_count += 1
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else: 
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alpha_beta_search(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break 
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alpha_beta_search(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break  
        return column, value



def alpha_beta_cutoff_search(board, depth, alpha, beta, maximizingPlayer, cutoff):
    global node_count
    node_count += 1
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal or depth >= cutoff:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:  
                return (None, 0)
        else:
           
            column = random.choice(valid_locations)
            return (column, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alpha_beta_cutoff_search(b_copy, depth + 1, alpha, beta, False, cutoff)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alpha_beta_cutoff_search(b_copy, depth + 1, alpha, beta, True, cutoff)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break 
        return column, value


def main():
    global selected_algo
    board = create_board()
    print_board(board)
    game_over = False
    turn = random.randint(PLAYER, AI)

    draw_board(board)
    draw_status(turn)
    draw_log()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, STATUS_BAR_HEIGHT))
                posx, posy = event.pos
                if turn == PLAYER and not game_over and BOARD_START_Y <= posy <= BOARD_START_Y + BOARD_HEIGHT:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = event.pos

               
                for algo_name, rect in algo_buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_algo = algo_name
                        draw_board(board)
                        draw_status(turn)
                        draw_log()
                        break  

              
                if start_button.collidepoint(event.pos):
                    board = create_board()
                    game_over = False
                    turn = random.randint(PLAYER, AI)
                    log_messages.clear()
                    draw_board(board)
                    draw_status(turn)
                    draw_log()
                    continue
                elif restart_button.collidepoint(event.pos):
                    board = create_board()
                    game_over = False
                    log_messages.clear()
                    draw_board(board)
                    draw_status(turn)
                    draw_log()
                    continue
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if not game_over:
                    
                    if turn == PLAYER:
                        if BOARD_START_Y <= posy <= BOARD_START_Y + BOARD_HEIGHT:
                            col = int(math.floor(posx / SQUARESIZE))

                            if col >= 0 and col < COLUMN_COUNT:
                                if is_valid_location(board, col):
                                    row = get_next_open_row(board, col)
                                    drop_piece(board, row, col, PLAYER_PIECE)

                                    if winning_move(board, PLAYER_PIECE):
                                        show_game_over("Player")
                                        game_over = True

                                    print_board(board)
                                    draw_board(board)
                                    draw_status(turn)
                                    draw_log()

                                    turn = AI
                                    draw_status(turn)

                                    if not game_over and len(get_valid_locations(board)) == 0:
                                        show_game_over("Draw")
                                        game_over = True
                        else:
                           
                            pass

        # AI's turn
        if turn == AI and not game_over:
            # Show AI's turn status
            draw_status(turn)
            pygame.display.update()

            # AI calculates move
            start_time = time.time()
            node_count = 0

            if selected_algo == "Random Move":
                col = get_random_move(board)
            elif selected_algo == "Minimax":
                col, minimax_score = minimax(board, 4, True)
            elif selected_algo == "Alpha-Beta":
                col, minimax_score = alpha_beta_search(board, 6, -math.inf, math.inf, True)
            elif selected_algo == "A-BCutoff":
                col, minimax_score = alpha_beta_cutoff_search(board, 0, -math.inf, math.inf, True, cutoff=5)
            else:
                col = get_random_move(board)

            end_time = time.time()
            search_time = end_time - start_time

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    show_game_over("AI")
                    game_over = True

                print_board(board)
                draw_board(board)
                draw_status(turn)

               
                log_messages.append(
                    f"AI ({selected_algo}) explored {node_count} nodes in {search_time:.2f} seconds."
                )
                draw_log()

                turn = PLAYER
                draw_status(turn)

                if not game_over and len(get_valid_locations(board)) == 0:
                    show_game_over("Draw")
                    game_over = True

        pygame.display.update()


if __name__ == "__main__":
    main()
