import pygame
import random

pygame.init()

width,height=700, 500
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Whack-a-Mole")
clock=pygame.time.Clock()


DARK_GREEN=(0, 150, 0)

mole=pygame.transform.scale(pygame.image.load("images/mole.png"),(100,100))

font_large=pygame.font.SysFont(None, 60)
font=pygame.font.SysFont(None, 40)

holes=[(100, 100), (300, 100), (500, 100),(100, 300), (300, 300), (500, 300)]

score=0
lives=5
level=1
mole_timer=0
mole_interval=1200    #time given to hit the mole
current_hole=random.choice(holes)
mole_visible=True
hit=False
active=True

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect=pygame.Rect(x, y, w, h)
        self.text=text

    def draw(self, surface):
        pygame.draw.rect(surface,"#00BD00", self.rect)
        txt=font.render(self.text, True, "#000000")
        text_rect=txt.get_rect(center=self.rect.center)
        surface.blit(txt, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

restart_button=Button(270, 280, 160, 50, "Play Again")

def draw_holes():
    for x, y in holes:
        pygame.draw.ellipse(screen, "#000000", (x+25, y+60, 50, 25))

def draw_mole(position):
    rect=mole.get_rect(center=(position[0]+50, position[1]+50))
    screen.blit(mole, rect)
    return rect

def draw_stats():
    score_text=font.render(f"Score: {score}", True, "#ffffff")
    lives_text=font.render(f"Lives: {lives}", True, "#ffffff")
    level_text=font.render(f"Level: {level}", True, "#ffffff")
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 60))
    screen.blit(level_text, (20, 100))

def game_over_screen():
    screen.fill("#000000")
    text1=font_large.render("Game Over!", True, "#ffffff")
    text2=font.render(f"Final Score: {score}", True, "#ffffff")
    screen.blit(text1, (235,150))
    screen.blit(text2, (260, 210))
    restart_button.draw(screen)

running=True
while running:
    screen.fill("#6fc466")
    if active:
        draw_holes()
        current_time=pygame.time.get_ticks()

        if current_time-mole_timer >mole_interval:
            if not hit:
                lives-=1
            current_hole=random.choice(holes)
            mole_timer=current_time
            mole_visible=True
            hit=False

        mole_rect=None

        if mole_visible:
            mole_rect=draw_mole(current_hole)

        draw_stats()
        if score>=level*10:
            level+=1
            mole_interval=max(300, mole_interval-100)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type ==pygame.MOUSEBUTTONDOWN:
                if mole_rect and mole_rect.collidepoint(event.pos):
                    if not hit:
                        score+=1
                        hit=True
                        mole_visible=False
        if lives<=0:
            active=False

    else:
        game_over_screen()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    score=0
                    lives=5
                    level=1
                    mole_interval=1000
                    mole_timer=pygame.time.get_ticks()
                    active=True
                    hit=False
                    current_hole=random.choice(holes)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
