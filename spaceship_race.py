import pygame
import time
import math
from utilsfile import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

BACKGROUND = pygame.image.load("Resources/Background_RCG.png")
TRACK = pygame.image.load("Resources/TrackComplete_RCG.png")

TRACK_BORDER = pygame.image.load("Resources/OnlyTrack_RCG.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("Resources/finish_RCG.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (400, 35)

RED_SHIP = scale_image(pygame.image.load("Resources/red_ship.png"), 0.6)
BLUE_SHIP = scale_image(pygame.image.load("Resources/blue_ship.png"), 0.6)

#setup display surface - should be the same size as track
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Race!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

#1b
FPS = 60
PATH = [(145, 61), (130, 220), (370, 165), (375, 280), (246, 400), (166, 359), (74, 656), (219, 632), (352, 535), (659, 542), (620, 395), (667, 265), (721, 139), (391, 72)]#, (237, 459), (116, 344), (69, 512), (158, 671), (339, 572), (589, 594), (741, 492), (560, 366), (755, 232), (720, 84), (389, 81)]
#setting up levels
class GameInfo:
    # set a limit to the ammount of levels
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
    
    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

#this isa base class for ships, both player and CPU.
class AbstractShip:

    # max_vel = maximum velocity, rotation_vel = rotation velocity - want to know how fast the ship is moving and turning
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 0.1


    def rotation(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x -x), int(self.y -y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0


class PlayerShip(AbstractShip):
    IMG=RED_SHIP
    START_POS = (340, 40)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class CpuShip(AbstractShip):
    IMG = BLUE_SHIP
    START_POS = (340, 75)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
    
    def draw(self, win):
        super().draw(win)
        #self.draw_points(win)
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else: 
            desired_radian_angle = math.atan(x_diff / y_diff)
        
        #fixing the angle if you need over accute angle (optuse)
        if target_y > self.y:
            desired_radian_angle += math.pi
        
        diff_in_angle = self.angle - math.degrees(desired_radian_angle)
        #if angle is over 180 it is likely an inefficient route
        if diff_in_angle >=180:
            diff_in_angle -= 360

        if diff_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(diff_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(diff_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1


    def move(self):
        #this ensures there is no index error moving to somewher that doesn't exist
        if self.current_point >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.25
        self.rotation_vel = self.rotation_vel + (level -1) * 0.25
        self.current_point = 0

    
#function fordrawing images in a window (the visuals inside the game window)
def draw(win, images, player_ship, cpu_ship, game_info):
    for img, pos in images:
        win.blit(img, pos)
    level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))
    
    vel_text = MAIN_FONT.render(f"Velocity: {round(player_ship.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_ship.draw(win)
    cpu_ship.draw(win)
    pygame.display.update()

def move_player(player_ship):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_ship.rotation(left=True)
    if keys[pygame.K_RIGHT]:
        player_ship.rotation(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_ship.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_ship.move_backward()

    if not moved:
        player_ship.reduce_speed()

def handle_collision(player_ship, cpu_ship, game_info):
    if player_ship.collide(TRACK_BORDER_MASK) != None:
        player_ship.bounce()


    cpu_finish_poi_collide = cpu_ship.collide(FINISH_MASK, *FINISH_POSITION)
    
    if cpu_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        #manual delay
        pygame.time.wait(5000)
        game_info.reset()
        player_ship.reset()
        cpu_ship.reset()

    player_finish_poi_collide = player_ship.collide(FINISH_MASK, *FINISH_POSITION)

    if player_finish_poi_collide != None:
        if player_finish_poi_collide[0] == 0:
            player_ship.bounce()
        else:
            game_info.next_level()
            player_ship.reset()
            cpu_ship.next_level(game_info.level)
            
        


#setting up the event loop -run keeps the window alive
run = True

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer (see 1b, 1c)
clock = pygame.time.Clock()
images = [(BACKGROUND, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_ship = PlayerShip(4, 4)
cpu_ship = CpuShip(2, 2, PATH)
game_info = GameInfo()

while run:
    #1c
    clock.tick(FPS)

    draw(WIN, images, player_ship, cpu_ship, game_info)
    # in Pygame 0,0 is top left corner, furthest right is max X value, furthest down is max Y value
    
    #update() is a method that needs to run every time to make sure everything is drawn

    #logic for starting the game


    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press and key to start level {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            if event.type == pygame.KEYDOWN:
                game_info.start_level()
    

    for event in pygame.event.get():
        #check if the user has the window open of closed
        if event.type == pygame.QUIT:
            run = False
            break

        

        # !!!FOR PLOTING CPU PATH!!!    
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #pos = pygame.mouse.get_pos()
            #cpu_ship.path.append(pos)
    

    move_player(player_ship)
    cpu_ship.move()

    handle_collision(player_ship, cpu_ship, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")

        #manual delay for text
        pygame.time.wait(5000)

        game_info.reset()
        player_ship.reset()
        cpu_ship.reset()



#print(cpu_ship.path)
pygame.quit()

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer
