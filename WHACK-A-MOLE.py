
import pygame
import random
import cv2
import mediapipe as mp
import sys
import os


pygame.init()


width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()


def load_image(path, scale=None):
    try:
        img = pygame.image.load(path)
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception as e:
        print(f"Failed to load image '{path}':", e)
        pygame.quit()
        sys.exit()

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Failed to load sound '{path}':", e)
        return None


mole_img = load_image("./images/mole.png", (100, 100))
fake_mole_img = load_image("./images/fake_mole.png", (100, 100))
incorrect_sound = load_sound("./sounds/wrong.mp3")


font_large = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 40)


holes = [(100,100),(300,100),(500,100),(700,100),(100,300),(300,300),(500,300),(700,300),(250,200),(550,200)]
colors = ("#18DEDB","#35ABD8","#FF6FE3","#6fc466","#306FE3","#30BA38","#99507F")
score = 0
lives = 5
level = 1
interval1 = 2200
interval2 = 1000
fake_interval = 1500
mole_duration = 2200
game_won = False
trail = []

arrival1 = pygame.time.get_ticks()
arrival2 = arrival1 + interval2
arrival_fake = arrival1 + fake_interval

hole1 = random.choice(holes)
hole2 = random.choice([h for h in holes if h != hole1])
fake_hole = random.choice([h for h in holes if h != hole1 and h != hole2])


try:
    HANDS = mp.solutions.hands
    hands = HANDS.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.7)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Webcam not accessible")
except Exception as e:
    print("Mediapipe initialization or webcam error:", e)
    pygame.quit()
    sys.exit()

visible1 = visible2 = fake_visible = False
hit1 = hit2 = hit_fake = False
active = True

class Button:
    def __init__(self, x, y, w, h, txt):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = txt
    def draw(self, surface):
        pygame.draw.rect(surface, "#00BD00", self.rect)
        txt = font.render(self.text, True, "#000000")
        surface.blit(txt, txt.get_rect(center=self.rect.center))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

restart_button = Button(360, 300, 160, 50, "Play Again")

def draw_holes():
    for x, y in holes:
        pygame.draw.ellipse(screen, "#000000", (x+25, y+60, 50, 25))

def draw_mole(pos, img):
    rect = img.get_rect(center=(pos[0]+50, pos[1]+50))
    screen.blit(img, rect)
    return rect

def draw_stats():
    screen.blit(font.render(f"Score: {score}", True, "#ffffff"), (20, 20))
    screen.blit(font.render(f"Lives: {lives}", True, "#ffffff"), (20, 60))
    screen.blit(font.render(f"Level: {level}", True, "#ffffff"), (20, 100))
    if error is not None:
        screen.blit(font.render(f"Pointer Error: {int(error)} px", True, "#ffffff"), (20, 380))
        screen.blit(font.render(f"Accuracy: {grade_text}", True, grade_color), (20, 420))

def game_over_screen():
    screen.fill("#000000")
    screen.blit(font_large.render("Game Over!", True, "#ffffff"), (315, 150))
    screen.blit(font.render(f"Final Score: {score}", True, "#ffffff"), (340, 210))
    restart_button.draw(screen)

def game_win_screen():
    screen.fill("#000000")
    screen.blit(font_large.render("Congratulations!", True, "#00FF00"), (280, 150))
    screen.blit(font.render("You completed all levels!", True, "#FFFFFF"), (280, 210))
    screen.blit(font.render(f"Final Score: {score}", True, "#FFFFFF"), (340, 250))
    restart_button.draw(screen)

running = True
while running:
    screen.fill(colors[level % len(colors)])
    if active:
        draw_holes()
        now = pygame.time.get_ticks()
        ret, frame = cap.read()
        if not ret:
            print("Webcam frame not received.")
            break

        frame = cv2.flip(frame, 1)
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)
        except Exception as e:
            print("Error processing hand tracking:", e)
            result = None

        hand_x, hand_y = None, None
        if result and result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                try:
                    index_tip = hand_landmarks.landmark[HANDS.HandLandmark.INDEX_FINGER_TIP]
                    hand_x = int(index_tip.x * width)
                    hand_y = int(index_tip.y * height)
                    if hand_x and hand_y:
                        trail.append((hand_x, hand_y))
                        if len(trail) > 30:
                            trail.pop(0)
                    pygame.draw.circle(screen, (255, 0, 0), (hand_x, hand_y), 10)
                except:
                    pass

        

        if visible1 and hand_x and hand_y:
            target_x, target_y = hole1[0] + 50, hole1[1] + 50
            error = ((hand_x - target_x) ** 2 + (hand_y - target_y) ** 2) ** 0.5
            if error < 30:
                grade_text = "Excellent"
                grade_color = (0, 255, 0)
            elif error < 60:
                grade_text = "Okay"
                grade_color = (255, 215, 0)
            else:
                grade_text = "Poor"
                grade_color = (255, 0, 0)
        else:
            error = None

        if not visible1 and now - arrival1 >= 0:
            hole1 = random.choice(holes)
            arrival1 = now
            visible1 = True
            hit1 = False
            departure1 = now + mole_duration

        if visible1 and now >= departure1:
            if not hit1:
                lives -= 1
                if incorrect_sound:
                    incorrect_sound.play()
            visible1 = False
            arrival2 = now + interval2

        if level >= 2 and not visible2 and now >= arrival2:
            hole2 = random.choice([h for h in holes if h != hole1])
            arrival2 = now
            visible2 = True
            hit2 = False
            departure2 = now + mole_duration

        if visible2 and now >= departure2:
            if not hit2:
                lives -= 1
                if incorrect_sound:
                    incorrect_sound.play()
            visible2 = False
            if level >= 3:
                arrival_fake = now + fake_interval

        if level >= 3 and not fake_visible and now >= arrival_fake:
            fake_hole = random.choice([h for h in holes if h != hole1 and h != hole2])
            arrival_fake = now
            fake_visible = True
            hit_fake = False
            departure_fake = now + mole_duration

        if fake_visible and now >= departure_fake:
            fake_visible = False

        rect1 = rect2 = rect_fake = None
        if visible1:
            rect1 = draw_mole(hole1, mole_img)
        if visible2:
            rect2 = draw_mole(hole2, mole_img)
        if fake_visible:
            rect_fake = draw_mole(fake_hole, fake_mole_img)

        draw_stats()

        if score >= level * 10:
            level += 1
            if level == 3:
                mole_duration += 500
            elif level > 3:
                active = False
                game_won = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if hand_x and hand_y:
            if rect1 and rect1.collidepoint((hand_x, hand_y)) and not hit1:
                score += 1
                hit1 = True
                visible1 = False
            if level >= 2 and rect2 and rect2.collidepoint((hand_x, hand_y)) and not hit2:
                score += 1
                hit2 = True
                visible2 = False
            if level >= 3 and rect_fake and rect_fake.collidepoint((hand_x, hand_y)) and not hit_fake:
                lives -= 1
                if incorrect_sound:
                    incorrect_sound.play()
                hit_fake = True
                fake_visible = False

        if lives <= 0:
            active = False

    else:
        if game_won:
            game_win_screen()
        else:
            game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    score = 0
                    lives = 5
                    level = 1
                    interval1 = 2200
                    interval2 = 1000
                    fake_interval = 1500
                    mole_duration = 2200
                    arrival1 = pygame.time.get_ticks()
                    visible1 = visible2 = fake_visible = False
                    hit1 = hit2 = hit_fake = False
                    game_won = False
                    active = True

    pygame.display.update()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
