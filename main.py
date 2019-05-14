import numpy as np
#from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey,ReleaseKey, A, D, SPACE
import win32gui, win32ui, win32con, win32api
import keyboard

width = 1024
height = 768
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

def draw_lines(processedimg, window):
        
    try: 
        lines = cv2.HoughLinesP(processedimg, rho=1, theta=np.pi/180, threshold=70, minLineLength=20, maxLineGap=2)
        for line in lines:
            coords = line[0]
            #print(coords)
            cv2.line(window, (coords[0],coords[1]), (coords[2],coords[3]), (0,255,0), 2, cv2.LINE_AA)
    except Exception as e:
        pass    

def draw_bombs(img, window):
        lower_red = (0,70,50)
        upper_red = (10,255,255)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #cv2.inRange(img_hsv, (0, 100, 100), (10, 255, 255), lower_red_hue_range)
        #cv2.inRange(img_hsv, (160, 100, 100), (179, 255, 255), upper_red_hue_range)
        #red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
        #red_hue_image = cv2.GaussianBlur(red_hue_image, (3, 3), 2, 2)
        mask = cv2.inRange(img_hsv, lower_red, upper_red) 
  
       
        res = cv2.bitwise_and(img,img, mask= mask) 
        # cv2.imshow('frame',img) 
        # cv2.imshow('mask',mask) 
        # cv2.imshow('res',res) 
        # bombs = cv2.HoughCircles(red_hue_image, 1, red_hue_image.rows/8, 100, 20, 0, 0)

        # try:
        #         for bomb in bombs:
        #                 print (bomb)
        #                 #radius = bomb[2]
        #                 #cv2.circle(window, center, radius, (0, 255, 0), 5)
                        
        # except Exception as e:
        #          print(e)
def edge_detect(original_img):
    # METHOD: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    sigma=0.33
    original_img = cv2.cvtColor(original_img,cv2.COLOR_BGR2GRAY)
    v = np.median(original_img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    processed_img = cv2.Canny(original_img, lower, upper)
    processed_img = cv2.GaussianBlur(processed_img, (3,3),0)
    #cv2.imshow('gaussian+canny',processed_img)
    vertices = np.array([[50,50],[750,50],[750,550],[50,550]])
    processed_img = roi(processed_img, [vertices])

    
    

    return processed_img



def screen_record(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    screen = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    #new_screen = edge_detect(screen)
    return screen

# def screen_record(): 
#     last_time = time.time()
#     while(True):
#         # 800x600 windowed mode
#         screen =  np.array(ImageGrab.grab(bbox=(0,40,800,625)))
#         new_screen = edge_detect(screen)
#         #print('loop took {} seconds'.format(time.time()-last_time))
#         last_time = time.time()
#         #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
#         cv2.imshow('Canny_window', new_screen)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break
last_time = time.time()
paused = False

while(True):
        if not paused:
                screen = screen_record(region=(0,40,width,height+40))
                canny_img = edge_detect(screen)
                draw_lines(canny_img, screen)
                draw_bombs(screen, screen)
                cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
                print('loop took {} seconds'.format(time.time()-last_time))
                last_time = time.time()
                if keyboard.is_pressed('p'):
                        paused = True
                        print("Paused...")
                        ReleaseKey(A)
                        ReleaseKey(SPACE)
                        ReleaseKey(D)
                        time.sleep(1)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
        else:
                if keyboard.is_pressed('u'):
                        paused = False
                        print("Continue...")
                        time.sleep(1)
