
import pygame
import random
import time
import os
import sys

pygame.init()
width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Card Flip Game')

# Load sounds with error handling
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return None

correct_sound = load_sound("./sounds/match.wav")
incorrect_sound = load_sound("./sounds/wrong.mp3")
flip_sound = load_sound("./sounds/cardflip.wav")
win_sound = load_sound("./sounds/applause.mp3")

# Load images with error handling
image_filenames = ["bee.jpg", "cat.jpg", "dog.jpg", "duck.jpg", "eagle.jpg", "monkey.jpg", "sheep.jpg", "turtle.jpg"]
card_images = []
for img in image_filenames:
    path = os.path.join("images", img)
    if not os.path.exists(path):
        print(f"Missing image file: {path}")
        pygame.quit()
        sys.exit()
    card_images.append(pygame.transform.scale(pygame.image.load(path), (130, 130)))

cards = card_images * 2
random.shuffle(cards)

# Load back image
try:
    card_back = pygame.transform.scale(pygame.image.load("images/back.jpg"), (100, 150))
except pygame.error as e:
    print(f"Error loading card back image: {e}")
    pygame.quit()
    sys.exit()

rows, cols = 4, 4
cardwidth = 100
margin = 15

flipped = []
matched = [False] * 16
positions = []  # holds x y coordinate of each card

for i in range(16):
    x = 5.5 * margin + (cardwidth + 3 * margin) * (i % cols)
    y = margin + (cardwidth + 4 * margin) * (i // cols)
    positions.append((x, y))

points = 5

def draw_card():
    screen.fill((94, 46, 72))
    for i, (x, y) in enumerate(positions):
        if matched[i] or i in flipped:
            screen.blit(cards[i], (x, y))
        else:
            screen.blit(card_back, (x, y))
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {points}", True, (255, 255, 255))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height - 42))
    pygame.display.flip()

def get_card_index(pos):
    x, y = pos
    for i, (cx, cy) in enumerate(positions):
        rect = pygame.Rect(cx, cy, cardwidth, cardwidth)
        if rect.collidepoint(x, y):
            if flip_sound:
                flip_sound.play()
            return i
    return None

running = True
while running:
    draw_card()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and len(flipped) < 2:
            i = get_card_index(event.pos)
            if i is not None and not matched[i] and i not in flipped:
                flipped.append(i)
                draw_card()

            if len(flipped) == 2:
                pygame.time.delay(800)
                a, b = flipped
                if cards[a] == cards[b]:
                    matched[a] = True
                    matched[b] = True
                    points += 5
                    if correct_sound:
                        correct_sound.play()
                else:
                    points -= 1
                    if incorrect_sound:
                        incorrect_sound.play()
                flipped = []

    if all(matched):
        screen.fill((0, 200, 0))
        font = pygame.font.SysFont(None, 72)
        lines = ["You Win!", "", f"Score: {points}"]
        y = height // 2 - 100
        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (width // 2 - text.get_width() // 2, y))
            y += text.get_height() + 10
        if win_sound:
            win_sound.play()
        pygame.display.flip()
        pygame.time.delay(5000)
        running = False

pygame.quit()
