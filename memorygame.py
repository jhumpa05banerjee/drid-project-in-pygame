import pygame
import random
import time
pygame.init()
width, height=700,700
screen=pygame.display.set_mode((width,height))

pygame.display.set_caption('Memory Game Card Flipping')

correct_sound=pygame.mixer.Sound("./sounds/match.wav")
incorrect_sound=pygame.mixer.Sound("./sounds/wrong.mp3")
flip_sound=pygame.mixer.Sound("./sounds/cardflip.wav")
win_sound=pygame.mixer.Sound("./sounds/applause.mp3")

images=["bee.jpg","cat.jpg","dog.jpg","duck.jpg","eagle.jpg","monkey.jpg","sheep.jpg","turtle.jpg"]
card_images=[];
for img in images:
    card_images.append(pygame.transform.scale(pygame.image.load(f"images/{img}"),(130,130)))

cards=[]
cards=card_images*2
random.shuffle(cards)

card_back=pygame.transform.scale(pygame.image.load("images/back.jpg"),(100,150))

rows,cols =4,4
cardwidth=100
margin=15

flipped=[]
matched=[False]*16
positions=[]   #holds x y coordinate of each card
for i in range(16):
    x=5.5*margin+(cardwidth+3*margin) * (i%cols)
    y=margin+(cardwidth+4*margin) * (i//cols)
    positions.append((x, y))


def draw_card():   #showing cards at positions
    screen.fill((94, 46, 72)) 
    for i, (x,y) in enumerate(positions):
        if matched[i] or i in flipped:
            screen.blit(cards[i],(x,y))
        else:
            screen.blit(card_back,(x,y))

    font = pygame.font.SysFont(None, 36)  //the score display
    score_text = font.render(f"Score: {points}", True, (255, 255, 255))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height - 42))

    pygame.display.flip()

def get_card_index(pos):
    x,y=pos
    for i, (cx, cy) in enumerate(positions):
        rect =pygame.Rect(cx, cy, cardwidth, cardwidth)
        if rect.collidepoint(x,y):
            flip_sound.play()
            return i
    return None


running=True
points=5
while running:
    draw_card()
    font = pygame.font.SysFont(None, 72)
    text = font.render(f"Score: {points}", True, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type ==pygame.MOUSEBUTTONDOWN and len(flipped) < 2:
            i= get_card_index(event.pos)
            if i is not None and not matched[i] and i not in flipped:
                flipped.append(i)
                draw_card()

            if len(flipped)==2:
                pygame.time.delay(800)  #showing the cards for a moment
                a,b=flipped
                if cards[a]==cards[b]:
                    matched[a]=True
                    matched[b]=True
                    points+=5
                    correct_sound.play()
                else:
                    if points>=2:
                        points=points-2
                    elif points==1:
                        points-=1
                    incorrect_sound.play()
                flipped=[]

    if all(matched):
        screen.fill((0, 200, 0))
        font = pygame.font.SysFont(None, 72)

        lines = ["You Win!", "", f"Score: {points}"]
        y = height // 2 - 100
        for line in lines:
            text=font.render(line, True, (255, 255, 255))
            screen.blit(text, (width // 2 - text.get_width() // 2, y))
            y+=text.get_height() + 10
            win_sound.play()
        pygame.display.flip()
        pygame.time.delay(5000)
        running = False
        pygame.quit()




