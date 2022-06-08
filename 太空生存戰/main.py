import pygame,random,os

#set attributes
FPS=60
WIDTH=500
HEIGHT=600

#set (R,G,B) to color 
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)

#pygame's initialization
pygame.init() 
pygame.mixer.init() #sound 
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#inlude image
background_img=pygame.image.load(os.path.join("img","background.png")).convert() #use convert() to change into faster format
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
player_mini_img=player_img.copy()
rock_imgs=[]
for i in range(7): rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
treasure_imgs={}
treasure_imgs["shield"]=pygame.image.load(os.path.join("img","shield.png")).convert()
treasure_imgs["lightning"]=pygame.image.load(os.path.join("img","gun.png")).convert()

#include animation
expl_anim={}
expl_anim['large_expl']=[]
expl_anim['small_expl']=[]
expl_anim['player_expl']=[]
for i in range(9):
    expl_img=pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['large_expl'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['small_expl'].append(pygame.transform.scale(expl_img,(30,30)))

    player_expl_img=pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player_expl'].append(player_expl_img)

#include sound
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
die_sound=pygame.mixer.Sound(os.path.join("sound","rumble.mp3"))
expl_sound=[]
for i in range(2): expl_sound.append(pygame.mixer.Sound(os.path.join("sound",f"expl{i}.wav")))
shield_sound=pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
lightning_sound=pygame.mixer.Sound(os.path.join("sound","pow1.wav"))

#include background music
pygame.mixer.music.load(os.path.join("sound","background.mp3 "))

#include time
clock=pygame.time.Clock()

#include font style
font_name=os.path.join("font.ttf")

#change image size
player_img=pygame.transform.scale(player_img,(50,38)) 
player_mini_img=pygame.transform.scale(player_img,(25,19))
 
#change color : black => transparent
player_img.set_colorkey(BLACK) 
player_mini_img.set_colorkey(BLACK)
bullet_img.set_colorkey(BLACK)
for i in range(7): rock_imgs[i].set_colorkey(BLACK)
treasure_imgs["shield"].set_colorkey(BLACK)
treasure_imgs["lightning"].set_colorkey(BLACK)

#set game window
pygame.display.set_caption("Game")
pygame.display.set_icon(player_mini_img)

#set volume
pygame.mixer.Sound.set_volume(shoot_sound,0.2) #0~1
pygame.mixer.Sound.set_volume(expl_sound[0],0.2)
pygame.mixer.Sound.set_volume(expl_sound[1],0.2)
pygame.mixer.Sound.set_volume(shield_sound,0.2)
pygame.mixer.Sound.set_volume(lightning_sound,0.2)
pygame.mixer.music.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        #set attributes to pygame's sprite
        pygame.sprite.Sprite.__init__(self) 

        #set image attributes
        self.image=player_img #set image
        self.rect=self.image.get_rect() #set border

        #set image's initialize position
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10

        #set other attributes
        self.speedx=8
        self.radius=20
        self.health=100
        self.lives=3
        self.hidden=False
        self.hide_time=0
        self.gun=1
        self.gun_time=0

    def update(self):
        now=pygame.time.get_ticks()
        if self.gun==2 and now-self.gun_time>5000:
            self.gun=1

        #if hide longer than 1s
        if self.hidden and now-self.hide_time>1000: 
            self.hidden=False
            #set to original coordinate
            self.rect.centerx=WIDTH/2 
            self.rect.bottom=HEIGHT-10

        #move
        key_press=pygame.key.get_pressed() #return a bool dictionary
        if key_press[pygame.K_LEFT]: #if press left 
            self.rect.x-=self.speedx
        if key_press[pygame.K_RIGHT]: #if press right
            self.rect.x+=self.speedx

        #let player always inside the border
        if self.rect.right>WIDTH: #if right hand side is out of right bound
            self.rect.right=WIDTH
        if self.rect.left<0: #if left hand side is out of left bound
            self.rect.left=0

    def shoot(self):
        #can't shoot in hidden period
        if self.hidden: return
        
        if self.gun == 1:
            bullet=Bullet(self.rect.centerx,self.rect.top) #create a bullet
            #add to sprites
            bullets.add(bullet)
            all_sprites.add(bullet)

            shoot_sound.play() #play shoot sound
        elif self.gun>=2:
            bullet1=Bullet(self.rect.left,self.rect.top) #create a bullet
            bullet2=Bullet(self.rect.right,self.rect.top) #create a bullet
            
            bullets.add(bullet1)
            all_sprites.add(bullet1)

            bullets.add(bullet2)
            all_sprites.add(bullet2)

            shoot_sound.play() #play shoot sound

    def hide(self):
        self.hidden=True
        self.hide_time=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+500) #set position out of bound, equals hidden

    def gun_up(self):
        self.gun=min(self.gun+1,2)
        self.gun_time=pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image_ori=random.choice(rock_imgs) #randomly choose one rock of different sizes

        #set image attributes
        self.image=self.image_ori
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-180,-100)

        #set other attributes
        self.radius=int(self.rect.width*0.85/2)
        self.speedx=random.randrange(-1,1)
        self.speedy=random.randrange(2,8)
        self.rot_degree=random.randrange(-3,3)
        self.total_degree=0
  
    
    def update(self):
        #update position and rotate degree
        self.rotate()
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy

        #if rock is out of bound, delete it and recreate a new rock
        if self.rect.top>HEIGHT or self.rect.right<0 or self.rect.left>WIDTH:
            self.kill()
            create_rock()

    def rotate(self):
        self.total_degree+=self.rot_degree #add rotate degrees
        self.total_degree=self.total_degree % 360

        self.image=pygame.transform.rotate(self.image_ori,self.total_degree) #use original image to rotate
        
        #record original center, and reposition to it
        center=self.rect.center 
        self.rect=self.image.get_rect()
        self.rect.center=center

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        #set image attributes
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y

        #set other attributes
        self.speedy=-10

    def update(self):
        self.rect.y+=self.speedy

        if self.rect.bottom<0: #if out of bound
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)

        #set self's attrbutes
        self.size=size
        self.center=center

        #set image attributes
        self.image=expl_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=self.center

        #set other attributes
        self.frame=0
        self.frame_interval=50
        self.last_update=pygame.time.get_ticks() #return time from init to now

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_interval:
            self.last_update=now
            self.frame+=1
            
            if self.frame==len(expl_anim[self.size]): #if to end the animation
                self.kill() #delete this animation element
            else:
                self.image=expl_anim[self.size][self.frame] #set to next frame

class Treasure(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)

        #set self's attributes
        self.type=random.choice(["shield","lightning"])
        self.center=center

        #set image attributes
        self.image=treasure_imgs[self.type]
        self.rect=self.image.get_rect()
        self.rect.center=self.center

        #set other attributes
        self.speedy=3

    def update(self):
        self.rect.y+=self.speedy

        if self.rect.bottom>HEIGHT: #if out of bound
            self.kill()

def create_rock():
    rock=Rock()

    #add to sprites
    rocks.add(rock)
    all_sprites.add(rock)

def draw_text(surf,text,size,x,y):
    #set font element
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)

    #set position
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y

    #draw text_surface at text_rect
    surf.blit(text_surface,text_rect) 

def draw_health(surf,hp,x,y):
    if hp<0: hp=0

    #set bar attributes
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=int(hp/100*BAR_LENGTH)

    #set rectangle attributes
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)

    pygame.draw.rect(surf,WHITE,outline_rect,2) #frame=2
    pygame.draw.rect(surf,GREEN,fill_rect) #filled

def draw_lives(surf,lives,x,y):
    for i in range(lives):
        img_rect=player_mini_img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y

        surf.blit(player_mini_img,img_rect)

def draw_menu():
    #draw init menu
    screen.blit(background_img,(0,0)) 
    draw_text(screen,"太空生存戰",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"左右鍵移動飛船，空白鍵發射子彈",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"按任意鍵開始",18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()

    #wait untill player press any key
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            elif event.type==pygame.KEYUP: #if player press any key
                return True

#init
score=0
running=True
init=True

#play the music
pygame.mixer.music.play(-1) #-1 = unlimited play

#start
while running:
    clock.tick(FPS) #do only FPS times in one second

    if init:
        start=draw_menu()
        if not start: break

        init=False
        #create sprites group
        all_sprites=pygame.sprite.Group() #all_sprites = rocks + bullets
        rocks=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        treasures=pygame.sprite.Group()

        #create a player
        player=Player()
        all_sprites.add(player) #add to all_sprites

        #create 8 rocks
        for _ in range(8): create_rock()

        score=0
    
    #get user's input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if quit pressed
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if space pressed
                player.shoot()

    #update all elements
    all_sprites.update()

    #if bullit hits rock
    bullet_hit_rock=pygame.sprite.groupcollide(rocks,bullets,True,True) #return a dictionary of collided pair
    for hit in bullet_hit_rock:
        create_rock() #recreate a rock

        score+=(100-hit.radius) #inscrase score

        #play explosion animation
        expl=Explosion(hit.rect.center,'large_expl')
        all_sprites.add(expl)
        random.choice(expl_sound).play() #play explosion sound

        #create treasure
        if random.random()<=0.1:
            treasure=Treasure(hit.rect.center)
            all_sprites.add(treasure)
            treasures.add(treasure)

    #if player is hitten by rock
    rock_hit_player=pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle) #use the circle method to determind colisions
    for hit in rock_hit_player:
        create_rock()

        player.health-=hit.radius #decrease life

        expl=Explosion(hit.rect.center,'small_expl')
        all_sprites.add(expl)

        #if die
        if player.health <= 0:
            player.lives-=1 #decrease live by one
            player.health=100 #reset health to 100
            player.hide() #hide player for 1s

            #play explosion animation
            death_expl_anim=Explosion(player.rect.center,'player_expl')
            all_sprites.add(death_expl_anim)
            die_sound.play()

    #if player eat the treasure
    treasure_hit_player=pygame.sprite.spritecollide(player,treasures,True)
    for hit in treasure_hit_player: 
        if hit.type == "shield": #if eat shield
            player.health+=20 #add blood
            if player.health>100: player.health=100
            shield_sound.play()
        elif hit.type=="lightning": #if eat lightning
            player.gun_up() #add to two bullets
            lightning_sound.play()

    #if no lives and animation is end
    if player.lives == 0 and not death_expl_anim.alive():
        init=True

    screen.blit(background_img,(0,0)) #draw background on screen
    all_sprites.draw(screen) #draw all elements on screen
    draw_text(screen,str(score),18,WIDTH/2,10) #draw score on screen
    draw_health(screen,player.health,5,15) #draw blood bar on screeen
    draw_lives(screen,player.lives,WIDTH-100,10) #draw lives on screen
    pygame.display.update() #display in the window

pygame.quit() #exit