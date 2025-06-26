
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

#background image
image=pygame.image.load("Neon_lights.png")
re_image=pygame.transform.scale(image,(WIDTH, HEIGHT))
#background music
mixer.music.load('Game music.wav')
mixer.music.play(-1)

# Colors
colors = [pygame.Color("red"), pygame.Color("blue"), pygame.Color("green"), pygame.Color("yellow")]
color_index = 0

# Player settings
player_radius = 30
player_x = WIDTH // 2
player_y = HEIGHT - 100

score = 0
font = pygame.font.Font('PressStart2P-Regular.ttf', 25)
new_game_timer = 0
flash_timer = 0
# Game state
running = True
game_over = False


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

# Main loop
while running:
    if pygame.time.get_ticks() - flash_timer < 200:
        pygame.draw.circle(screen, colors[color_index], (player_x, player_y), player_radius + 20, 4)
    screen.blit(re_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                click=mixer.Sound("click.wav")
                click.play()
                color_index = (color_index + 1) % len(colors)
            if event.key == pygame.K_r:
                score=0
                new_game_timer = pygame.time.get_ticks()
                color_index=0
                game_over = False
                obstacles.clear()

    if new_game_timer != 0 and pygame.time.get_ticks() - new_game_timer < 500:
        new_game_text = font.render("New Game Started", True, pygame.Color("cyan"))
        screen.blit(new_game_text, (WIDTH // 2 - new_game_text.get_width() // 2, HEIGHT // 2 - 100))

    pygame.draw.line(screen, colors[color_index], (0, player_y), (WIDTH, player_y), 2)
    score_text = font.render(f"Score: {score}", True, pygame.Color("white"))
    screen.blit(score_text, (10, 10))

    if not game_over:
        # Draw player
        pygame.draw.circle(screen, colors[color_index], (player_x, player_y), player_radius)

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= 60:
            obstacles.append(Obstacle())
            spawn_timer = 0

        # Create player rect for collision detection
        player_rect = pygame.Rect(0, 400, 80, 30)

        # Update obstacles
        # Check if obstacle crosses player's Y position (within a margin)
        player_line_y = player_y  # fixed line level

        for obstacle in obstacles[:]:
            obstacle.move()
            obstacle.draw(screen)

            # Trigger when obstacle enters player line
            if player_line_y - 10 < obstacle.y + obstacle.height < player_line_y + 10:
                if obstacle.color != colors[color_index]:
                    fail = Sound("Fail sound.wav")
                    fail.play()
                    game_over = True
                    print("💥 Game Over! Wrong color on line.")
                else:
                    flash_timer = pygame.time.get_ticks()
                    score += 1
                    obstacles.remove(obstacle)

            # Clean up off-screen
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
    else:
        # Game Over screen
        text = font.render("Game Over! Press R to Restart", True, pygame.Color("white"))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        score_text = font.render(f"Score: {score}", True, pygame.Color("white"))
        screen.blit(score_text, (10, 10))

        # Restart logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            obstacles.clear()
            color_index = 0
            score=0
            new_game_timer = pygame.time.get_ticks()

    if pygame.time.get_ticks() - flash_timer < 50:
        # Flash with current color
        screen.fill(colors[color_index])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
