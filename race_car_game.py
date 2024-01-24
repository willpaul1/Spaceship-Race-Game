import time
import random
import keyboard

def clear_screen():
    print("\033c", end="")

def draw_car(car_position):
    print("\n" * (car_position -1) + "^")

def draw_obstacle(obstacle_position):
    print(" " * obstacle_position + "*")

def main():
    screen_height, screen_width= stdscr.getmaxyx()
    car_position = 10
    obstacle_position = random.randint(1, 20)
    score = 0

    while True:
        clear_screen()

        draw_car(car_position)
        draw_obstacle(obstacle_position)

        print(f"Score: {score}")

        obstacle_position += 1

        # Check for collision
        if car_position == obstacle_position:
            print("Game Over!")
            time.sleep(2)
            break

        # Check if obstacle reached the bottom
        if obstacle_position >= 20:
            obstacle_position = 0
            score += 1

        time.sleep(0.1)

        # Get user input
        if keyboard.is_pressed('right') and car_position < 20:
            car_position += 1
        elif keyboard.is_pressed('left') and car_position > 0:
            car_position -= 1
        elif keyboard.is_pressed('up') and car_position > 1:
            car_position -= 1
        elif keyboard.is_pressed('down') and car_position < 20:
            car_position += 1

if __name__ == "__main__":
    main()