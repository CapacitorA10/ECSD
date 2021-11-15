##
import cv2
import matplotlib.pyplot as plt
import numpy as np
print(cv2.__version__)

## image read
img = cv2.imread('lane_l.png')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img = cv2.GaussianBlur(img, (3,3),0) #일부러 가우시안 입히기
plt.imshow(img, cmap='gray')
plt.show()
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

edge = cv2.Canny(img, 50, 200)
plt.imshow(edge, cmap='gray')
mask = region_interest(edge)
plt.imshow(mask, cmap='gray')
plt.show()

## hough line detect
def draw_lines(img, lines, color=[255,0,0], thickness=5):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                            minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_imge = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint8)
    draw_lines(line_imge, lines)
    return line_imge

rho = 2
theta = np.pi/180
threshold = 20
min_line_len = 50
max_line_gap = 150

lines = cv2.cvtColor(hough_lines(mask, rho, theta, threshold, min_line_len, max_line_gap), cv2.COLOR_RGB2GRAY)

plt.imshow(lines, cmap='gray')
plt.show()

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

decision = RL_search(img)
##

