import pygame
import time
import math
from utilsfile import scale_image, blit_rotate_center


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

#1b
FPS = 60
PATH = [(272, 81), (158, 75), (73, 124), (72, 233), (181, 249), (278, 203), (459, 199), (481, 284), (372, 312), (304, 370), (264, 459), (166, 450), (162, 352), (70, 348), (61, 523), (88, 664), (173, 670), (268, 642), (291, 569), (378, 561), (609, 552), (708, 537), (719, 446), (614, 411), (593, 339), (690, 303), (735, 209), (718, 103), (590, 80), (459, 78), (386, 84)]

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
        self.draw_points(win)
    
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
    
#function fordrawing images in a window (the visuals inside the game window)
def draw(win, images, player_car, cpu_ship):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
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



#setting up the event loop -run keeps the window alive
run = True

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer (see 1b, 1c)
clock = pygame.time.Clock()
images = [(BACKGROUND, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_ship = PlayerShip(4, 4)
cpu_ship = CpuShip(4, 4, PATH)

while run:
    #1c
    clock.tick(FPS)

    draw(WIN, images, player_ship, cpu_ship)
    # in Pygame 0,0 is top left corner, furthest right is max X value, furthest down is max Y value
    
    #update() is a method that needs to run every time to make sure everything is drawn
    

    for event in pygame.event.get():
        #check if the user has the window open of closed
        if event.type == pygame.QUIT:
            run = False
            break

        # !!!FOR PLOTING CPU PATH!!!    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cpu_ship.path.append(pos)
    
    keys = pygame.key.get_pressed()
    moved = False

    move_player(player_ship)
    cpu_ship.move()

    if player_ship.collide(TRACK_BORDER_MASK) != None:
        player_ship.bounce()

    finish_poi_collide = player_ship.collide(FINISH_MASK, *FINISH_POSITION)

    if finish_poi_collide != None:
        if finish_poi_collide[0] == 0:
            player_ship.bounce()
        else:
            player_ship.reset()
            print("Finish")
        


print(cpu_ship.path)
pygame.quit()

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer
