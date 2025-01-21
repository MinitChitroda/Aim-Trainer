import pygame
pygame.init()
import random
import math
import time


pygame.mixer.init()

LIVES = 20
WIDTH, HEIGHT = 800, 600
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 20)
TITLE_FONT = pygame.font.SysFont("comicsans", 40)  #for difficulty screen
pygame.display.set_caption("AIM TRAINER")
GUNSHOTS = [pygame.mixer.Sound("sound1.mp3"), pygame.mixer.Sound("sound2.mp3")]
DIFFICULTY_LEVELS = {
    "EASY": 600,
    "MEDIUM": 400,
    "HARD": 250
}

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    COLOR1 = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):  # this function creates a target "RING SHAPED"
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size))  # surface, color, position on the surface, size
        pygame.draw.circle(win, self.COLOR1, (self.x, self.y), int(self.size * 0.8))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size * 0.6))
        pygame.draw.circle(win, self.COLOR1, (self.x, self.y), int(self.size * 0.4))

    def collide(self, x, y):
        dist = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return dist <= self.size

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def play_gunshot():
    random.choice(GUNSHOTS).play()

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/sec", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

# Added new function for difficulty selection screen
def draw_button(win, text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, hover_color, button_rect)
    else:
        pygame.draw.rect(win, color, button_rect)
    
    pygame.draw.rect(win, "white", button_rect, 2)
    text_surface = LABEL_FONT.render(text, 1, "white")
    win.blit(text_surface, (x + width/2 - text_surface.get_width()/2,
                           y + height/2 - text_surface.get_height()/2))
    return button_rect

def difficulty_screen():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        WIN.fill(BG_COLOR)
        
        title = TITLE_FONT.render("Select Difficulty", 1, "white")
        WIN.blit(title, (WIDTH/2 - title.get_width()/2, 100))
        
        button_width, button_height = 200, 50
        button_x = WIDTH/2 - button_width/2
        
        easy_rect = draw_button(WIN, "EASY", button_x, 200, button_width, button_height, (0, 100, 0), (0, 150, 0))
        medium_rect = draw_button(WIN, "MEDIUM", button_x, 300, button_width, button_height, (100, 100, 0), (150, 150, 0))
        hard_rect = draw_button(WIN, "HARD", button_x, 400, button_width, button_height, (100, 0, 0), (150, 0, 0))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    return "EASY"
                if medium_rect.collidepoint(mouse_pos):
                    return "MEDIUM"
                if hard_rect.collidepoint(mouse_pos):
                    return "HARD"

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    #play again and quit buttons
    button_width, button_height = 200, 50
    play_again_rect = draw_button(WIN, "Play Again", WIDTH/2 - button_width - 20, 500,
                                button_width, button_height, (0, 100, 0), (0, 150, 0))
    quit_rect = draw_button(WIN, "Quit", WIDTH/2 + 20, 500,
                          button_width, button_height, (100, 0, 0), (150, 0, 0))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    return True
                if quit_rect.collidepoint(mouse_pos):
                    return False

def main():
    playing = True
    
    while playing:
        difficulty = difficulty_screen()
        if difficulty is None: 
            break
            
        target_increment = DIFFICULTY_LEVELS[difficulty]
        
        run = True
        targets = []
        clk = pygame.time.Clock()
        target_pressed = 0
        clicks = 0
        misses = 0
        start_time = time.time()

        pygame.time.set_timer(TARGET_EVENT, target_increment)

        while run:
            clk.tick(60)  # 60 frames per second
            click = False
            elapsed_time = time.time() - start_time
            mouse_pos = pygame.mouse.get_pos()  # Update mouse position

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == TARGET_EVENT:
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)  # generates a random position ensuring that they don't appear off the screen
                    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    target = Target(x, y)  # initializing an instance of the Target class
                    targets.append(target)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True  # Correctly set click to True
                    clicks += 1  # Increment clicks counter

            for target in targets:
                target.update()

                if target.size <= 0:
                    targets.remove(target)
                    misses += 1

                if click and target.collide(*mouse_pos):
                    play_gunshot()
                    targets.remove(target)
                    target_pressed += 1

            if misses >= LIVES:
                playing = end_screen(WIN, elapsed_time, target_pressed, clicks)
                run = False
                continue

            draw(WIN, targets)
            draw_top_bar(WIN, elapsed_time, target_pressed, misses)
            pygame.display.update()

    pygame.quit()

try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to close...")  # This keeps the window open