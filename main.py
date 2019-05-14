import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey,ReleaseKey, A, D, SPACE


# # gives us time to get situated in the game
for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)
# while(True):
#     # PressKey(A)  
#     # time.sleep(1)
#     # ReleaseKey(A)
#     # time.sleep(1)

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            print(coords)
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), (255,255,255), 2)
    except Exception as e:
        pass        

def process_img(original_img):
    # METHOD: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    sigma=0.33
    v = np.median(original_img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    processed_img = cv2.Canny(original_img, lower, upper)
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    vertices = np.array([[50,50],[750,50],[750,550],[50,550]])
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 50, 150, 30, 5)
    draw_lines(processed_img, lines)

    return processed_img



def screen_record(): 
    last_time = time.time()
    while(True):
        # 800x600 windowed mode
        screen =  np.array(ImageGrab.grab(bbox=(0,40,800,625)))
        new_screen = process_img(screen)
        #print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        cv2.imshow('Canny_window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()