import pygame
import random
import sys
from pygame import mixer
from pygame.mixer import Sound

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Swap Dodger")
clock = pygame.time.Clock()

# Load background
bg_image = pygame.image.load("Neon_lights.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Load sounds
mixer.music.load('Game music.wav')
mixer.music.play(-1)
click_sound = Sound("click.wav")
fail_sound = Sound("Fail sound.wav")

# Fonts
font = pygame.font.Font('PressStart2P-Regular.ttf', 25)

# Colors (neon-pink palette)
colors = [
    pygame.Color(176, 38, 255),
    pygame.Color(255, 16, 240),
    pygame.Color(31, 81, 255),
    pygame.Color(255, 255, 0)
]
color_index = 0

# Player setup
player_radius = 30
player_x = WIDTH // 2
player_y = HEIGHT - 100
score = 0

# Game state
game_state = "menu"  # "playing", "paused", "game_over"
flash_timer = 0
new_game_timer = 0


# Obstacle class
class Obstacle:
    def __init__(self):
        self.width = 80
        self.height = 30
        self.x = random.randint(100, WIDTH - 100)
        self.y = -self.height
        self.color = random.choice(colors)
        self.speed = 5

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > HEIGHT


# Obstacle list
obstacles = []
spawn_timer = 0

# Game loop
running = True
while running:
    screen.blit(bg_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    game_state = "playing"
                    score = 0
                    color_index = 0
                    obstacles.clear()

            elif game_state == "playing":
                if event.key == pygame.K_SPACE:
                    click_sound.play()
                    color_index = (color_index + 1) % len(colors)
                elif event.key == pygame.K_p:
                    game_state = "paused"

            elif game_state == "paused":
                if event.key == pygame.K_p:
                    game_state = "playing"

            elif game_state == "game_over":
                if event.key == pygame.K_r:
                    game_state = "playing"
                    score = 0
                    color_index = 0
                    obstacles.clear()
                    new_game_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_m:
                    game_state = "menu"

    #Game State Handling

    if game_state == "menu":
        title_text = font.render("Color Swap Dodger", True, pygame.Color("white"))
        start_text = font.render("Press ENTER to Start", True, pygame.Color("yellow"))
        instr_text = font.render("SPACE = Switch Color | P = Pause", True, pygame.Color("cyan"))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2 + 40))

    elif game_state == "paused":
        pause_text = font.render("PAUSED", True, pygame.Color("yellow"))
        resume_text = font.render("Press P to Resume", True, pygame.Color("white"))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 20))

    elif game_state == "game_over":
        over_text = font.render("GAME OVER", True, pygame.Color("red"))
        score_text = font.render(f"Score: {score}", True, pygame.Color("gold"))
        retry_text = font.render("Press R to Restart | M for Menu", True, pygame.Color("white"))

        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 40))

    elif game_state == "playing":
        # Flash text for new game
        if new_game_timer != 0 and pygame.time.get_ticks() - new_game_timer < 1500:
            new_game_text = font.render("New Game Started", True, pygame.Color("white"))
            screen.blit(new_game_text, (WIDTH // 2 - new_game_text.get_width() // 2, HEIGHT // 2 - 100))

        # Draw color line
        pygame.draw.line(screen, colors[color_index], (0, player_y), (WIDTH, player_y), 2)

        # Draw player
        pygame.draw.circle(screen, pygame.Color("white"), (player_x, player_y), player_radius + 5)
        pygame.draw.circle(screen, colors[color_index], (player_x, player_y), player_radius)

        # Score display
        score_text = font.render(f"Score: {score}", True, pygame.Color("white"))
        screen.blit(score_text, (10, 10))

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= 60:
            obstacles.append(Obstacle())
            spawn_timer = 0

        player_line_y = player_y
        for obstacle in obstacles[:]:
            obstacle.move()
            obstacle.draw(screen)

            # Check collision line
            if player_line_y - 10 < obstacle.y + obstacle.height < player_line_y + 10:
                if obstacle.color != colors[color_index]:
                    fail_sound.play()
                    game_state = "game_over"
                else:
                    flash_timer = pygame.time.get_ticks()
                    score += 1
                    obstacles.remove(obstacle)

            if obstacle.is_off_screen():
                obstacles.remove(obstacle)

        #glow ring when color matched
        if pygame.time.get_ticks() - flash_timer < 200:
            pygame.draw.circle(screen, colors[color_index], (player_x, player_y), player_radius + 20, 4)

    # Flip the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
