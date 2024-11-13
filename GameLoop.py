import pygame
import os
import random
from operator import attrgetter
from random import uniform
from random import randint
import time

pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT= 750,750
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pygame: Space Invaders")
BG = pygame.image.load(os.path.join("res","BG.png"))
BG2 = pygame.image.load(os.path.join("res","BG.png"))
PLAYER_SHIP= pygame.image.load(os.path.join("res","PlayerShip.png"))
ALIEN_1= pygame.image.load(os.path.join("res","Alien1.png"))
ALIEN_2= pygame.image.load(os.path.join("res","Alien2.png"))
ALIEN_3= pygame.image.load(os.path.join("res","Alien3.png"))
LASER_RED= pygame.image.load(os.path.join("res","LaserRed.png"))
LASER_BLUE= pygame.image.load(os.path.join("res","LaserBlue.png"))
LASER_YELLOW= pygame.image.load(os.path.join("res","LaserYellow.png"))
SHIELD_GREEN= pygame.image.load(os.path.join("res","ShieldGreen.png"))
SHIELD_YELLOW= pygame.image.load(os.path.join("res","ShieldYellow.png"))
SHIELD_RED= pygame.image.load(os.path.join("res","ShieldRed.png"))

LASER_SOUND = pygame.mixer.Sound(os.path.join("res", "laser.wav"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("res", "explosion.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("res", "hit.wav"))

SPEED= pygame.image.load(os.path.join("res","speed_boost.png"))
COOLDOWN= pygame.image.load(os.path.join("res","rapid.png"))

BGy=0
BG2y = 0- HEIGHT
scrollSpeed = 2
   
class Particle(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: tuple,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 600

        # Ensure create_surf is called
        self.create_surf()

    def create_surf(self):
        # Create the surface with alpha channel
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(2, 2), radius=2)
        self.rect = self.image.get_rect(center=self.pos)

    def move(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > 2000 or
            self.pos[1] < -50 or
            self.pos[1] > 2000
        ):
            self.kill()

    def update(self, dt):
        self.move()
        self.fade(dt)
        self.check_pos()
        self.check_alpha()   
   

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    def move(self,vel):
        self.y += vel
    def off_screen(self,height):
        return  not (self.y <= height and self.y>=0)
    
    def collision(self,obj):
        
        return collide(obj,self)
    
class Ship:
    particle_group = pygame.sprite.Group() 
    COOLDOWN = 30
    
    def __init__(self,x,y,health=100):
        self.x= x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
        
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
        
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    
    def move_lasers(self, vel, obj,textArr):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
           
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-= 10
                self.lasers.remove(laser)
                textArr.append(FloatingText("HP: "+str(obj.health), (obj.x + obj.get_width() / 2, obj.y), (255, 0, 0)))
                HIT_SOUND.play()
                
                
    def check_lasers(self, vel, obj):
        for laser in self.lasers:
            if laser.collision(obj):
                obj.health-= 10
                self.lasers.remove(laser)
                
    #checks cooldown for lasers         
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter =0
        elif self.cool_down_counter>0:
            self.cool_down_counter +=1
            
    #creates a laser that the ship will fire
    def shoot(self):
        if self.cool_down_counter == 0:
            laser= Laser(self.x+self.ship_img.get_width()/2 -self.laser_img.get_width()/2,self.y,self.laser_img)
            LASER_SOUND.play()
            self.lasers.append(laser)
            self.cool_down_counter=1
       
    #spawns particles for various uses of the ship     
    def spawn_particles(self, n: int, x: int, y: int, directionBounds=[-1,1,-1,1], color= (255,255,255)):
        for _ in range(n):
              
            direction = pygame.math.Vector2(uniform(directionBounds[0],directionBounds[1]),uniform(directionBounds[2],directionBounds[3]))  # Slight random direction
            speed = random.randint(1, 3)
            Particle(self.particle_group, [x, y], color, direction, speed)
    
#subclass of ship
class Player(Ship):
    COOLDOWN = 30
    speed_boost = False
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)   
        self.ship_img= PLAYER_SHIP
        self.laser_img = LASER_BLUE
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = 100
        self.active_powerups = {}
        self.base_vel =5
        self.vel = self.base_vel 

    def update_powerups(self):
        #Handle timed expiration of power-ups.
        current_time = pygame.time.get_ticks()
        if "cooldown" in self.active_powerups:
            # Reset cooldown after duration
            if current_time - self.active_powerups["cooldown"] > Powerup.DURATION:
                self.COOLDOWN = 40  # Reset to default
                del self.active_powerups["cooldown"]

        if "speed" in self.active_powerups:
            # Reset speed boost after duration
            if current_time - self.active_powerups["speed"] > Powerup.DURATION:
                self.speed_boost = False
                self.vel = self.base_vel  # Reset to default
                del self.active_powerups["speed"]
                
    def move_lasers(self, vel, objs):
        self.cooldown()
        self.update_powerups()  # Update any active power-up effects
        #move lasers that ship has fired
        for laser in self.lasers:
            laser.move(vel)
            
            if not laser.off_screen(HEIGHT):
                #check for laser collisions with other ships or shield
                for obj in objs: 
                    if laser.collision(obj):
                        obj.health -=10
                        self.lasers.remove(laser)
            else:
                self.lasers.remove(laser)
                        
#class for flating text graphics               
class FloatingText:
    def __init__(self, text, pos, color=(255, 255, 255), font_size=20):
        self.text = text
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.alpha = 255  
        self.font = pygame.font.Font(os.path.join("res", "ka1.ttf"), font_size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.pos)
        self.fade_speed = 7
        self.move_speed = -2  

    def update(self):
        # Move text upwards and reduce opacity
        self.pos.y += self.move_speed
        self.alpha -= self.fade_speed
        self.image.set_alpha(self.alpha)
        self.rect.center = self.pos

    def is_faded(self):
        return self.alpha <= 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)   
 
#subclass of ship
class Enemy(Ship):
    COLOR_MAP={"alien1":(ALIEN_1,LASER_RED),"alien2":(ALIEN_2,LASER_YELLOW),"alien3":(ALIEN_3,LASER_YELLOW)}
    def __init__(self, x,y,color,health=10):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.COLOR_MAP[color]
        self.mask= pygame.mask.from_surface(self.ship_img)
    
    def move(self,velX,velY):
        self.y+=velY
        self.x+=velX
        
#Method to handle collisions of objects in game      
def collide(obj1,obj2):
       offset_x = obj2.x -obj1.x
       offset_y = obj2.y - obj1.y
       return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None
   
class Powerup:
    # Different power-up types
    POWERUP_TYPES = {
        "cooldown": COOLDOWN,
        "speed": SPEED
    }
    DURATION = 5000  # Duration of power-up effect in milliseconds 

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.image = self.POWERUP_TYPES[type]
        self.mask= pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.vel = 3

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def apply(self, player):
        #Apply the power-up effect to the player based on type.
        if self.type == "cooldown":
            player.COOLDOWN = max(10, player.COOLDOWN - 20)  # Reduce cooldown
        elif self.type == "speed":
            player.speed_boost = True  
            player.vel = player.vel + 3  

    def collide(obj1, obj2):
        #Check for collision
        offset_x = obj2.x -obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None
        
#class for player shields
class Shield:
    
    COLOR_MAP={"green": SHIELD_GREEN,"yellow": SHIELD_YELLOW,"red": SHIELD_RED}
    
    def __init__(self,x,y,color, health =100):
        self.x= x
        self.y = y
        self.health = health
        self.color= color
        self.shield_img = self.COLOR_MAP[color]
        self.mask= pygame.mask.from_surface(self.shield_img)
        
    def draw(self,window):
        self.shield_img = self.COLOR_MAP[self.color]
        window.blit(self.shield_img,(self.x,self.y))
        
    def get_width(self):
        return self.shield_img.get_width()
    def get_height(self):
        return self.shield_img.get_height()
        
    def collide(obj1,obj2):
       offset_x = obj2.x -obj1.x
       offset_y = obj2.y - obj1.y
       return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None
   
   
       
        
     
def main():
    
    run = True
    FPS= 60
    clock = pygame.time.Clock()
    
    #Interface Elements
    level = 0
    lives = 3
    score = 0
    main_font = pygame.font.Font(os.path.join("res","ka1.ttf"), 30)
    lost_font = pygame.font.Font(os.path.join("res","ka1.ttf"), 40)
    floating_texts = []
    
    player = Player(300,650)
    enemies= []
    dir = 1
    
    #dimensions of enemy group
    enemyRow = 4
    enemyCol = 11
    #offset of enemies
    offset = (WIDTH/enemyCol)
    shields = []
    shield_num = 3 
    shield_offset = (WIDTH/shield_num)
    
    enemy_vel = 1
    laser_vel = 5
    lost=False
    lost_count = 0
    powerups =[]
    
    pygame.mixer.music.load(os.path.join("res", "Music_Loop.ogg"))
    pygame.mixer.music.play(-1)  # Loop music indefinitely
   
    
    def redraw_window():
        
        global BGy
        global BG2y
        
        #moves backgound down
        BGy+=scrollSpeed
        BG2y+=scrollSpeed
        
        #creates infinite scrolling bg effect
        if(BGy>=HEIGHT):
            BGy = BG2y-HEIGHT
            
        if(BG2y>=HEIGHT):
            BG2y = BGy-HEIGHT
        
        window.blit(BG,(0,BGy))
        window.blit(BG2,(0,BG2y))
        
        #render text info
        lives_label = main_font.render(f"Lives: {lives}", 1, (200, 0, 200))
        level_label = main_font.render(f"Level: {level}", 1, (200, 0, 200))
        score_label = main_font.render(f"Score: {score}", 1, (200, 0, 200))

        
        for enemy in enemies:
            enemy.draw(window)
        
       
            
        player.draw(window)
        
        for shield in shields:
            shield.draw(window)
        
        if lost == True:
            lost_label = lost_font.render("You Lost!!",1,(255,0,0))
            window.blit(lost_label,((WIDTH/2 - lost_label.get_width()/2),350))
            
        # Draw and update particles
        player.particle_group.update(clock.get_time() / 1000)  # Update particles
        player.particle_group.draw(window)  # Draw particles   
       
        window.blit(lives_label,(10,HEIGHT-10-lives_label.get_height())) 
        window.blit(level_label,(WIDTH-level_label.get_width()-10,HEIGHT-10-lives_label.get_height()))
        window.blit(score_label,(WIDTH/2-score_label.get_width()/2,HEIGHT-10-lives_label.get_height()))
        
        for powerup in powerups:
            powerup.draw(window)
            
        for text in floating_texts[:]:
            text.update()
            if text.is_faded():
                floating_texts.remove(text)
            else:
                text.draw(window)
                
        pygame.display.flip()
        
    while run:
        clock.tick(FPS)
        
        redraw_window()
        enemy_vel=0
        
        #check lose condition
        if lives<=0 :
            lost=True
            lost_count+=1
            
        if(player.health<=0):
            lives-=1
            player.health = 100
            
        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue
            
         #regenerate shields at the end of the level
        if (len(shields) == 0 and len(enemies)==0):
            
            shield_pos=75
            for i in range (shield_num):
                
                shield = Shield(shield_pos,2*HEIGHT/3,"green")
                shields.append(shield)
                shield_pos+=shield_offset
                
        #spawn enemies when cleared     
        if len(enemies) == 0:
            level += 1
            enemy_vel+=1
            rowPos=0
            for x in range(enemyRow):
                
                alienType= random.choice(["alien1","alien2","alien3"])
                colPos=0
                for y in range(enemyCol):
                    
                    enemy = Enemy(colPos,rowPos, alienType)
                    enemies.append(enemy)
                    colPos+=offset
                rowPos+=offset
            
                    
                
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
                
        # input handling
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - player.vel>0:
            player.y-=player.vel
            
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y+player.vel+player.get_height()<HEIGHT:
            player.y+=player.vel
            
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player.vel > 0:
            player.x-=player.vel
            
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player.vel+ player.get_width()<WIDTH:
            player.x+=player.vel
            
        if(keys[pygame.K_SPACE]):
            player.shoot()
            
        
        enemies.sort(key=attrgetter("x"))
        
        #shift enemy group if at edge of screen
        if(enemies[len(enemies)-1].x+enemies[len(enemies)-1].ship_img.get_width()>=WIDTH):
                    enemy_vel=level
                    dir=-1
        if(enemies[0].x<=0):
                    enemy_vel=level
                    dir= 1            
        for enemy in enemies[:]:
            
            #move enemies left and right
            if(FPS%60==0 ):
                enemy.move(.25*dir,enemy_vel)
            #move lasers that enemies have fires   
            enemy.move_lasers(laser_vel,player,floating_texts)
            
            #check if lasers hit any shields
            for shield in shields:
                enemy.check_lasers(laser_vel,shield)
                if shield.health ==0:
                    shields.remove(shield)
                if shield.health <60 and shield.health>30:
                    shield.color="yellow"
                if shield.health<30:
                    shield.color="red"
            
                
            #randomly have enemies shoot
            if random.randrange(0,70*FPS)==1:
                enemy.shoot() 
            #if player collides with enemy damage player and remove enemy    
             
            #handle enemy death
            if enemy.health <= 0:
                enemies.remove(enemy)
                EXPLOSION_SOUND.play()
                score += 10
                floating_texts.append(FloatingText("10", (enemy.x + enemy.get_width() / 2, enemy.y), (0, 255, 200)))
                enemy.spawn_particles(200, int(enemy.x + enemy.ship_img.get_width() / 2), int(enemy.y + enemy.ship_img.get_height()), [-1, 1, -1, 1])
                if random.random() < 0.2:
                    powerup_type = random.choice(["cooldown", "speed"])
                    powerup = Powerup(enemy.x, enemy.y, powerup_type)
                    powerups.append(powerup)
                    # Add floating text at the enemy’s position
                    floating_texts.append(FloatingText(powerup_type, (enemy.x + enemy.get_width() / 2, enemy.y), (0, 255, 200)))
            if collide(enemy,player):
                player.health-=10  
                enemies.remove(enemy)
                floating_texts.append(FloatingText("HP: "+str(player.health), (player.x + player.get_width() / 2, enemy.y), (255, 0, 0)))
               
            elif enemy.y + enemy.get_height()>HEIGHT:
                enemies.remove(enemy)
                lives-=1
        #handle powerups
        for powerup in powerups[:]:
            powerup.y+=powerup.vel
            if powerup.collide(player):
                powerup.apply(player)
                player.active_powerups[powerup.type] = pygame.time.get_ticks()  # Record activation time
                powerups.remove(powerup)
            if powerup.y>=HEIGHT:
                powerups.remove(powerup)
        player.spawn_particles(20,int(player.x+player.ship_img.get_width()/3),int(player.y+player.ship_img.get_height()-5),[-0.4, 0.4,1,1],(0,255,255))    
        player.spawn_particles(20,int(player.x+2*player.ship_img.get_width()/3),int(player.y+player.ship_img.get_height()-5),[-.4,.4,1,1],(0,255,255))      
        player.move_lasers(-laser_vel,enemies)
        



def main_menu():
    instruction_font = pygame.font.Font(os.path.join("res","ka1.ttf"),40)
    title_font = pygame.font.Font(os.path.join("res","ka1.ttf"),30)
    run  = True
    while run:
        window.blit(BG,(0,0))
       
        title_label = title_font.render("Pygame Invaders From Space!",1,(0,255,0))
        instruction_label = instruction_font.render("Press Any Key to Begin...",1,(0,255,0))
        window.blit(instruction_label,(WIDTH/2 -instruction_label.get_width()/2,350))
        window.blit(title_label,(WIDTH/2 -title_label.get_width()/2,20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()  
main_menu() 