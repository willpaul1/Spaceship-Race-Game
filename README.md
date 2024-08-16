# Python Pygame - Spaceship Race Game

Simple pygame example showcasing the following knowledge:
Pixel Perfect Collision
Path based navigation - Machine Plotting.
Mathmatical and Physics Principles: calculating momentum and 360 navigation of objects - example below

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


Created in Python using pygame.
