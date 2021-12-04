
import cv2
import matplotlib.pyplot as plt
import numpy as np
import lanetools as lt
import time


## image read
def imread(i,t):
    img = cv2.imread(f'lanes/{i+1}.png')
    img = cv2.GaussianBlur(img, (3,3),1) #일부러 가우시안 입히기
    #cv2.imshow('img',img)

    # csv 변환
    extracted_img = lt.color_extraction(img)
    #cv2.imshow('extracted',extracted_img)

    # Edge Detection
    edge = cv2.Canny(extracted_img, 80, 200)
    mask = lt.region_interest(edge)
    #plt.imshow(mask, cmap='gray')

    # original hough line
    lines = lt.hough_lines(mask,threshold=90)
    #cv2.imshow('hough',lines)

    # R-L search
    decision = lt.RL_search(cv2.cvtColor(lines, cv2.COLOR_RGB2GRAY))
    print(f"decision:{decision}")
    time.sleep(t)
    return decision
##

