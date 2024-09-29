import time
import board
import busio
import adafruit_adxl34x
import random

# Initialize I2C and the accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)
#acc.enable_freefall_detection(threshold=4, time=25)
#acc.enable_motion_detection(threshold=15)
#acc.enable_tap_detection(tap_count=1, threshold=5, duration=10, latency=10, window=255)
#acc.range = adafruit_adxl34x.Range.RANGE_2_G

ball_position = [10, 10]
max_x, max_y = 20, 20 # grid size
score = 0

food_position = [random.randint(0, max_x - 1), random.randint(0, max_y - 1)]
bad_position = [random.randint(0, max_x - 1), random.randint(0, max_y - 1)]

def draw_ball(position):
    print("\033[H\033[J") 
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == tuple(position):
                print("O", end=" ")
            elif (x, y) == tuple(food_position):
                print("@", end=" ") 
            elif (x, y) == tuple(bad_position):
                print("#", end=" ") 
            else:
                print(".", end=" ") 
        print()  
    print(f"SCORE: {score}")  

# start text
print("\033[H\033[J")
time.sleep(1)
print("WELCOME TO...")
time.sleep(1)
print("""
  _______ ______ _____  __  __ _____ _   _  ____  __  __ ______ _______ ______ _____  
 |__   __|  ____|  __ \|  \/  |_   _| \ | |/ __ \|  \/  |  ____|__   __|  ____|  __ \ 
    | |  | |__  | |__) | \  / | | | |  \| | |  | | \  / | |__     | |  | |__  | |__) |
    | |  |  __| |  _  /| |\/| | | | | . ` | |  | | |\/| |  __|    | |  |  __| |  _  / 
    | |  | |____| | \ \| |  | |_| |_| |\  | |__| | |  | | |____   | |  | |____| | \ \ 
    |_|  |______|_|  \_\_|  |_|_____|_| \_|\____/|_|  |_|______|  |_|  |______|_|  \_\
""")
time.sleep(3)

while True:

    x, y, z = acc.acceleration
    
    ball_position[0] -= int(x) 
    ball_position[1] += int(y) 

    ball_position[0] = max(0, min(max_x - 1, ball_position[0]))
    ball_position[1] = max(0, min(max_y - 1, ball_position[1]))

    if ball_position == food_position:
        score += 1  
        food_position = [random.randint(0, max_x - 1), random.randint(0, max_y - 1)]

    if ball_position == bad_position:
        print("\033[H\033[J") # clear terminal
        time.sleep(1) 
        print("""
   _____          __  __ ______    ______      ________ _____
  / ____|   /\   |  \/  |  ____|  / __ \ \    / /  ____|  __ \ 
 | |  __   /  \  | \  / | |__    | |  | \ \  / /| |__  | |__) |
 | | |_ | / /\ \ | |\/| |  __|   | |  | |\ \/ / |  __| |  _  /
 | |__| |/ ____ \| |  | | |____  | |__| | \  /  | |____| | \ \ 
  \_____/_/    \_\_|  |_|______|  \____/   \/   |______|_|  \_\ 
        """)
        time.sleep(1)
        print("Game Over! Your final score is:", score)
        break

    draw_ball(ball_position)

    time.sleep(0.1)

