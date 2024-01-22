import curses
import time
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    height, width = stdscr.getmaxyx()
    car = '^'
    car_y, car_x = height - 1, width // 2
    obstacle = '*'
    obstacle_y, obstacle_x = 0, random.randint(1, width - 2)
    score = 0

    while True:
        stdscr.clear()

        # Display the car
        stdscr.addch(car_y, car_x, car)

        # Display the obstacle
        stdscr.addch(obstacle_y, obstacle_x, obstacle)

        # Display the score
        stdscr.addstr(0, 0, f"Score: {score}")

        # Move the obstacle down
        obstacle_y += 1

        # Check for collision
        if car_y == obstacle_y and car_x == obstacle_x:
            stdscr.addstr(height // 2, width // 2 - 5, "Game Over!")
            stdscr.refresh()
            time.sleep(2)
            break

        # Check if obstacle reached the bottom
        if obstacle_y == height - 1:
            obstacle_y = 0
            obstacle_x = random.randint(1, width - 2)
            score += 1

        stdscr.refresh()
        time.sleep(0.1)

        # Get user input
        key = stdscr.getch()

        # Move the car based on user input
        if key == curses.KEY_RIGHT and car_x < width - 1:
            car_x += 1
        elif key == curses.KEY_LEFT and car_x > 0:
            car_x -= 1

if __name__ == "__main__":
    curses.wrapper(main)
