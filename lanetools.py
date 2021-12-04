import cv2
import numpy as np

YELLOW_LOW  = np.asarray([20, 100, 100])
YELLOW_HIGH = np.asarray([30, 255, 255])
WHITE_LOW   = np.asarray([0, 0, 160])
WHITE_HIGH  = np.asarray([50, 80, 255])

def color_extraction(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv, YELLOW_LOW, YELLOW_HIGH)
    white_mask = cv2.inRange(hsv, WHITE_LOW, WHITE_HIGH)
    mask = cv2.bitwise_or(yellow_mask, white_mask)
    # cv2.imshow('',threshold)

    return cv2.bitwise_and(img, img, mask=mask)

def region_interest(edge):

    mask = np.zeros_like(edge)

    if len(edge.shape)>2:
        channel_count = edge.shape[2]
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

def RL_search(img):
    y, x = img.shape
    search_point = np.asarray([x//2, (4*y)//5]) #가로 중간, 세로 4/5지점
    search_line = img[search_point[1],:] # 해당 지점의 가로줄 추출
    idx = (np.where(search_line>0) - search_point[0]).squeeze() # 해당 지점의 가로줄 유효값 추출
    if not((idx > 0).any()) :
        print('Right lane not detected')
        return 'n'
    if not((idx < 0).any()) :
        print('left lane not detected')
        return 'n'

    right_min = abs(idx[np.where(idx * (idx>0))[0][0]]).mean()
    left_min = abs(idx[np.where(idx * (idx<0))[0][-1]]).mean()
    # 우측이 더 멀다 = 우측으로 가야함 = 'r' return
    ret = 'r' if right_min>left_min else 'l'
    if right_min==left_min or abs(right_min-left_min)<20: ret='n'

    return ret
