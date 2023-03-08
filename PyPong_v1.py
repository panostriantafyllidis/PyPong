import pygame
import random
import time

# initialize Pygame
pygame.init()

# set screen dimensions
screen_width = 900
screen_height = 500

# set paddle dimensions
paddle_width = 20
paddle_height = 100
paddle_speed = 5

# set ball dimensions
ball_size = 10
ball_speed = 5

# set colors
white = (255, 255, 255)
black = (0, 0, 0)

# set font
font = pygame.font.SysFont('calibri', 50)

# set sound effects
bounce_sound = pygame.mixer.Sound("sfx/bounce.wav")
score_sound = pygame.mixer.Sound("sfx/score.wav")


# create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# create paddles
player1_paddle = pygame.Rect(
    50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
player2_paddle = pygame.Rect(screen_width - 50 - paddle_width,
                             screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# create ball
ball = pygame.Rect(screen_width // 2 - ball_size // 2,
                   screen_height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x = ball_speed * random.choice((1, -1))
ball_speed_y = ball_speed * random.choice((1, -1))

# set scores
score1 = 0
score2 = 0

# create center line
center_line = pygame.Rect(screen_width // 2 - 2, 0, 4, screen_height)

# draw game objects


def draw_game():
    screen.fill(black)
    pygame.draw.rect(screen, white, player1_paddle)
    pygame.draw.rect(screen, white, player2_paddle)
    pygame.draw.rect(screen, white, ball)
    pygame.draw.rect(screen, white, center_line)

    score_text = font.render(str(score1) + ' - ' + str(score2), True, white)
    score_rect = score_text.get_rect(center=(screen_width//2, 50))
    screen.blit(score_text, score_rect)

# update ball position


def update_ball():
    global ball_speed_x, ball_speed_y, score1, score2

    # check collision with walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        score2 += 1
        score_sound.play()
        ball_restart()
    if ball.right >= screen_width:
        score1 += 1
        score_sound.play()
        ball_restart()

    # check collision with paddles
    if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
        ball_speed_x *= -1
        bounce_sound.play()

    # update ball position
    ball.x += ball_speed_x
    ball.y += ball_speed_y

# restart ball position


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width//2, screen_height//2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    time.sleep(2)

# update paddle position


def update_paddle(paddle, up_key, down_key):
    keys = pygame.key.get_pressed()
    if keys[up_key] and paddle.top > 0:
        paddle.y -= paddle_speed
    if keys[down_key] and paddle.bottom < screen_height:
        paddle.y += paddle_speed


# game loop
running = True
clock = pygame.time.Clock()

while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update paddles and ball
    update_paddle(player1_paddle, pygame.K_w, pygame.K_s)
    update_paddle(player2_paddle, pygame.K_UP, pygame.K_DOWN)
    update_ball()

    # draw game objects
    draw_game()

    # update display
    pygame.display.flip()

    # set frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()
