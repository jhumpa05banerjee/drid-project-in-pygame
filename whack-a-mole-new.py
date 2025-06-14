import pygame
import random

pygame.init()

width, height=900,500
screen =pygame.display.set_mode((width, height))
pygame.display.set_caption("Whack-a-Mole")
clock =pygame.time.Clock()

mole_img= pygame.transform.scale(pygame.image.load("images/mole.png"), (100, 100))
fake_mole_img= pygame.transform.scale(pygame.image.load("images/fake_mole.png"), (100, 100))
font_large= pygame.font.SysFont(None, 60)
font= pygame.font.SysFont(None, 40)

holes= [(100, 100), (300, 100), (500, 100), (700, 100),(100, 300), (300, 300), (500, 300), (700, 300),(250, 200), (550, 200)]
colors= ("#18DEDB", "#35ABD8", "#FF6FE3", "#6fc466", "#306FE3", "#30BA38", "#99507F")

score =0
lives =5
level =1
interval1= 2200
interval2= 1000
fake_interval= 1500
mole_duration= 2200
game_won= False

arrival1= pygame.time.get_ticks()
arrival2= arrival1 + interval2
arrival_fake= arrival1 + fake_interval

hole1= random.choice(holes)
hole2= random.choice(holes)
fake_hole= random.choice(holes)
while hole2==hole1:
    hole2= random.choice(holes)
while fake_hole== hole1 or fake_hole == hole2:
    fake_hole= random.choice(holes)

visible1= False
visible2= False
fake_visible= False
hit1= False
hit2= False
hit_fake= False
active= True

class Button:
    def __init__(self, x, y, w, h, txt):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = txt
    def draw(self, surface):
        pygame.draw.rect(surface, "#00BD00", self.rect)
        txt = font.render(self.text, True, "#000000")
        rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

restart_button= Button(360, 300, 160, 50, "Play Again")

def draw_holes():
    for x, y in holes:
        pygame.draw.ellipse(screen, "#000000",(x+25, y+60, 50, 25))

def draw_mole(pos, img):
    rect= img.get_rect(center=(pos[0]+50, pos[1]+50))
    screen.blit(img, rect)
    return rect

def draw_stats():
    screen.blit(font.render(f"Score: {score}", True, "#ffffff"), (20, 20))
    screen.blit(font.render(f"Lives: {lives}", True, "#ffffff"), (20, 60))
    screen.blit(font.render(f"Level: {level}", True, "#ffffff"), (20, 100))

def game_over_screen():
    screen.fill("#000000")
    screen.blit(font_large.render("Game Over!", True, "#ffffff"), (315, 150))
    screen.blit(font.render(f"Final Score: {score}", True, "#ffffff"), (340, 210))
    restart_button.draw(screen)

def game_win_screen():
    screen.fill("#000000")
    text1= font_large.render("Congratulations!", True, "#00FF00")
    text2= font.render("You completed all levels!", True, "#FFFFFF")
    text3= font.render(f"Final Score: {score}", True, "#FFFFFF")
    screen.blit(text1, (280, 150))
    screen.blit(text2, (280, 210))
    screen.blit(text3, (340, 250))
    restart_button.draw(screen)

running= True
while running:
    screen.fill(colors[level % len(colors)])
    if active:
        draw_holes()
        now= pygame.time.get_ticks()

        if not visible1 and now - arrival1 >= 0:
            hole1= random.choice(holes)
            arrival1= now
            visible1= True
            hit1= False
            departure1= now + mole_duration

        if visible1 and now >=departure1:
            if not hit1:
                lives-= 1
            visible1= False
            arrival2= now + interval2

        if level>= 2 and not visible2 and now>= arrival2:
            hole2= random.choice(holes)
            while hole2==hole1:
                hole2= random.choice(holes)
            arrival2= now
            visible2= True
            hit2= False
            departure2= now + mole_duration

        if visible2 and now>= departure2:
            if not hit2:
                lives-= 1
            visible2= False
            if level>= 3:
                arrival_fake= now+fake_interval

        if level>= 3 and not fake_visible and now>= arrival_fake:
            fake_hole= random.choice(holes)
            while fake_hole== hole1 or fake_hole == hole2:
                fake_hole= random.choice(holes)
            arrival_fake= now
            fake_visible= True
            hit_fake= False
            departure_fake= now + mole_duration

        if fake_visible and now>= departure_fake:
            fake_visible= False

        rect1=rect2=rect_fake= None
        if visible1:
            rect1= draw_mole(hole1, mole_img)
        if visible2:
            rect2= draw_mole(hole2, mole_img)
        if fake_visible:
            rect_fake= draw_mole(fake_hole, fake_mole_img)

        draw_stats()

        if score>= pow(level-1,2)*10:
            level+=1
            if level> 3:
                active= False
                game_won= True
            interval1= max(700, interval1 - 100)
            interval2= max(400, interval2 - 50)
            fake_interval= max(500, fake_interval - 50)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running= False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if rect1 and rect1.collidepoint(event.pos) and not hit1:
                    score+= 1
                    hit1= True
                    visible1= False
                elif rect2 and rect2.collidepoint(event.pos) and not hit2:
                    score+= 1
                    hit2= True
                    visible2= False
                elif rect_fake and rect_fake.collidepoint(event.pos) and not hit_fake:
                    score= max(0, score - 2)
                    hit_fake= True
                    fake_visible= False

        if lives<= 0:
            active= False
    else:
        if game_won:
            game_win_screen()
        else:
            game_over_screen()

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                running= False
            if event.type== pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    score=0
                    lives=5
                    level=1
                    interval1=2200
                    interval2=1000
                    fake_interval=1500
                    mole_duration=1500
                    arrival1=pygame.time.get_ticks()
                    visible1=visible2=fake_visible=False
                    hit1= hit2=hit_fake = False
                    game_won=False
                    active=True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
