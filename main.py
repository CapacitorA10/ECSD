##
import cv2
import matplotlib.pyplot as plt
import numpy as np
print(cv2.__version__)
YELLOW_LOW  = np.asarray([20, 100, 100])
YELLOW_HIGH = np.asarray([30, 255, 255])
WHITE_LOW   = np.asarray([0, 0, 230])
WHITE_HIGH  = np.asarray([255, 80, 255])

## image read
img = cv2.imread('lane.png')
#img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img = cv2.GaussianBlur(img, (3,3),0) #일부러 가우시안 입히기
cv2.imshow('img',img)

## csv 변환
def color_extraction(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv, YELLOW_LOW, YELLOW_HIGH)
    white_mask = cv2.inRange(hsv, WHITE_LOW, WHITE_HIGH)
    mask = cv2.bitwise_or(yellow_mask, white_mask)
    # cv2.imshow('',threshold)

    return cv2.bitwise_and(img, img, mask=mask)

extracted_img = color_extraction(img)
cv2.imshow('extracted',extracted_img)

## Edge Detection

def region_interest(edge):

    mask = np.zeros_like(edge)

    if len(edge.shape)>2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    imshape = edge.shape
    region_of_interest_vertices = np.array([[(0,imshape[0]),
                                  (imshape[1]//2, imshape[0]//2),
                                  (imshape[1]//2, imshape[0]//2),
                                  (imshape[1], imshape[0])]],
                                   dtype=np.int32)


    cv2.fillPoly(mask, region_of_interest_vertices, ignore_mask_color)
    return cv2.bitwise_and(edge, mask)

edge = cv2.Canny(extracted_img, 50, 200)
plt.imshow(edge, cmap='gray')
mask = region_interest(edge)
plt.imshow(mask, cmap='gray')
plt.show()

## houghp line detect
'''
def draw_linesp(img, lines, color=[0,0,255], thickness=2):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1), (x2, y2), color, thickness)

def houghp_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                            minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_imge = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint8)
    draw_linesp(line_imge, lines)
    return line_imge

rho = 2
theta = np.pi/180
threshold = 20
min_line_len = 50
max_line_gap = 150

lines = houghp_lines(mask, rho, theta, threshold, min_line_len, max_line_gap)

cv2.imshow('hough',lines)
'''
## original hough line
def draw_lines(img, lines, color=[0,0,255], thickness=2):
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(mask, origin=0, threshold=55):
    lines = cv2.HoughLines(mask, 1, np.pi / 180, threshold)
    line_img = origin#
    if line_img == 0 : line_img = np.zeros((mask.shape[0], mask.shape[1],3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

lines =hough_lines(mask,threshold=55)
cv2.imshow('hough',lines)

## R-L search

def RL_search(img):
    y, x = img.shape
    search_point = np.asarray([x//2, (4*y)//5]) #가로 중간, 세로 4/5지점
    search_line = lines[search_point[1],:] # 해당 지점의 가로줄 추출
    idx = (np.where(search_line>0) - search_point[0]).squeeze() # 해당 지점의 가로줄 유효값 추출
    if not((idx > 0).any()) :
        print('Right lane not detected')
        return 'n'
    if not((idx < 0).any()) :
        print('left lane not detected')
        return 'n'

    right_min = abs(idx[np.where(idx * (idx>0))[0][0]])
    left_min = abs(idx[np.where(idx * (idx<0))[0][-1]])
    # 우측이 더 멀다 = 우측으로 가야함 = 'r' return
    ret = 'r' if right_min>left_min else 'l'
    if right_min==left_min: ret='n'

    return ret

decision = RL_search(cv2.cvtColor(lines, cv2.COLOR_RGB2GRAY))
##

