import cv2
import random
import numpy as np
import queue
from _collections import deque
from matplotlib import pyplot as plt
# img1 = cv2.imread('papaya1.jpg')
# img1 = cv2.imread('papaya2.jpg')
img1 = cv2.imread('papaya3.jpg')
gray1 = cv2.cvtColor(img1,0)
#resimg1 = cv2.resize(img1,(,),interpolation=cv2.INTER_CUBIC)
b1,g1,r1 = cv2.split(img1)
# cv2.imwrite('papaya3_b1.jpg', b1)
# cv2.imwrite('papaya3_g1.jpg', g1)
# cv2.imwrite('papaya2_r1.jpg', r1)
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
h1, s1, v1 = cv2.split(hsv)
# cv2.imwrite('papaya3_hsv.jpg', hsv)


# edge1 = cv2.Canny(g1, 100, 200)
# plt.imshow(g1, cmap='gray')
# plt.imshow(edge1, cmap='gray')
# plt.show()
g1 = cv2.GaussianBlur(g1,(3,3),0)
# g1 = cv2.medianBlur(g1,3)
# edges = cv2.Canny(g1, 50, 0)

# contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)


# edges2 = np.zeros((h,w),np.uint8)
edges2 = cv2.Canny(g1, 70, 0)   #try 70
h, w = edges2.shape[:2]
blank = np.zeros((h,w),np.uint8)

# edges2 = cv2.merge([blank,edges2,blank])
# usedblank = cv2.merge([blank,blank,blank])
# cv2.imwrite('papaya3_findcontours.jpg', edges2)


qhw = deque()
acheck = np.zeros((h,w),np.uint8)

dirup = dirdown = dirleft = dirright = 0
dirupleft = dirupright = dirdownleft = dirdownright = 0

def resetconstant():
    global dirup,dirdown,dirleft,dirright
    global dirupleft,dirupright,dirdownleft,dirdownright
    dirup = dirdown = dirleft = dirright = 0
    dirupleft = dirupright = dirdownleft = dirdownright = 0
def testconstant(para1):
    k=0
    global dirup,dirdown,dirleft,dirright
    global dirupleft,dirupright,dirdownleft,dirdownright
    if dirup>para1:
        k+=1
    if dirdown>para1:
        k += 1
    if dirleft>para1:
        k += 1
    if dirright>para1:
        k += 1
    if dirupleft>para1:
        k += 1
    if dirupright>para1:
        k += 1
    if dirdownleft>para1:
        k += 1
    if dirdownright>para1:
        k += 1
    return k

def search1(jh,jw):
    global dirup, dirdown, dirleft, dirright
    global dirupleft, dirupright, dirdownleft, dirdownright
    if edges2[jh][jw]!=0 and acheck[jh][jw]==0:
        if (jh,jw) not in qhw:
            qhw.append((jh,jw))
        acheck[jh][jw] = 255
        if edges2[jh+1][jw] != 0 and jh<h-2:
            search1(jh+1,jw)
            dirdown+=1;
            # print('Up')
            # print(jh+1,jw)
        if edges2[jh-1][jw] != 0 and jh>0:
            search1(jh - 1, jw)
            dirup+=1
            # print('Down')
            # print(jh - 1, jw)
        if edges2[jh][jw-1] != 0 and jw>0:
            search1(jh, jw - 1)
            dirleft+=1
            # print('Left')
            # print(jh, jw - 1)
        if edges2[jh][jw+1] != 0 and jw<w-2:
            search1(jh, jw + 1)
            dirright+=1
            # print('Right')
            # print(jh, jw + 1)
        # # 8 connection------
        # if edges2[jh+1][jw+1] != 0 and jh<h-2 and jw<w-2:
        #     search1(jh+1,jw+1)
        #     dirdownright+=1
        #     #Down Right
        # if edges2[jh-1][jw+1] != 0 and jh>0 and jw<w-2:
        #     search1(jh - 1, jw+1)
        #     dirupright+=1
        #     #Up Right
        # if edges2[jh-1][jw-1] != 0 and jh>0 and jw>0:
        #     search1(jh-1, jw - 1)
        #     dirupleft+=1
        #     #Up Left
        # if edges2[jh+1][jw-1] != 0 and jh<h-2 and jw>0:
        #     search1(jh+1, jw - 1)
        #     dirdownleft+=1
        #     #Down Left
def runsearch(hmax,wmax,para1,para2,para3):
    for jh in range(0,hmax-1):
        for jw in range(0,wmax-1):
            if acheck[jh][jw] == 0:
                search1(jh,jw)
                # print(len(qhw))
                if para3==True:
                    if testconstant(para2) >= 3:
                        for qhwele in qhw:
                            acheck[qhwele[0]][qhwele[1]] = 1
                        resetconstant()
                    else:
                        resetconstant()
                if len(qhw)<para1:
                    for qhwele in qhw:
                        acheck[qhwele[0]][qhwele[1]] = 1

                # print(qhw)
                qhw.clear()
                # print('www')

# runsearch(h,w,0,50,True)
# ret,acheck = cv2.threshold(acheck,127,255,cv2.THRESH_BINARY)    #clear all pixels' value == 1
edges2[0,:] = 255
edges2[h-1,:] = 255
edges2[:,0] = 255
edges2[:,w-1] = 255
# contours, hierarchy = cv2.findContours(acheck,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
contours, hierarchy = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
paint2 = np.zeros((h,w),np.uint8)

# paint2 = cv2.merge([blank,blank,blank])   #bgr
k=0
for i in contours:

    if k%20==0:
        # color1 = random.randint(0, 256)
        color2 = random.randint(0, 256)
        # color3 = random.randint(0, 256)
    if (len(i) > 50):  # 200
        cv2.drawContours(paint2, i, -1,255,5)
        # cv2.drawContours(paint2, i, -1,color2,5)
        cv2.boundingRect(i)
        k+=1

# cv2.imwrite('papaya3_drawcontour_line5.jpg', paint2)

# edges2 = paint2[:,:].copy()
# acheck = np.zeros((h,w),np.uint8)
# runsearch(h,w,5,0,False)
paint2[0,:] = 255
paint2[h-1,:] = 255
paint2[:,0] = 255
paint2[:,w-1] = 255
contours, hierarchy = cv2.findContours(paint2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
paint3 = np.zeros((h,w),np.uint8)


# paint3 = cv2.merge([blank,acheck,paint3]) #!!!!
edges3 = cv2.merge([edges2,edges2,edges2])

paint4 = np.zeros((h, w), np.uint8)
paint5 = np.zeros((h, w), np.uint8)
# paint4 = cv2.merge([paint4,paint4,paint4])
for i in range(len(contours)):
    if cv2.contourArea(contours[i]) > 5000 and cv2.contourArea(contours[i])<100000:
        hull = cv2.convexHull(contours[i])
        # length = len(hull)
        # for ihull in range(len(hull)):
        #     # cv2.line(paint3, tuple(hull[ihull][0]), tuple(hull[(ihull + 1) % length][0]), (color1,color2,color3), 2)
        #     cv2.line(paint3, tuple(hull[ihull][0]), tuple(hull[(ihull + 1) % length][0]), color1, 2)
        #     cv2.line(g1, tuple(hull[ihull][0]), tuple(hull[(ihull + 1) % length][0]), (0, 255, 255), 2)  # g1 hull
        epsilon = 0.01 * cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        print(len(approx))
        corners = len(approx)
        if corners > 5:
            ellipse = cv2.fitEllipse(contours[i])

            # ellipse_small = (ellipse[0], (ellipse[1][0] / 1.5, ellipse[1][1] / 1.2), ellipse[2])
            # cv2.ellipse(acheck, ellipse_small, (127, 127, 0), 2)
            # cv2.ellipse(g1, ellipse_small, (127, 127, 0), 2)

            cnt = contours[i]
            c_min = []
            c_min.append(cnt)

            color1 = random.randint(0, 256)
            color2 = random.randint(0, 256)
            color3 = random.randint(0, 256)
            cv2.drawContours(paint4, c_min, -1, 255, thickness=cv2.FILLED)

            kernel = np.ones((10, 10), np.uint8)
            erosion = cv2.erode(paint4, kernel, iterations=1)
            contours4, hierarchy4 = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for i4 in range(len(contours4)):
                if cv2.contourArea(contours4[i4]) > 3000:
                    cv2.drawContours(g1, contours4[i4], -1, 255, 1)
                    cv2.drawContours(paint5, contours4[i4], -1, 255, 1)
                    cv2.drawContours(img1, contours4[i4], -1, (color1,color2,color3), 1)

            # cv2.fillPoly(paint4,i,(255,255,255))
            # cv2.drawContours(g1, cnt, -1, (color1, color2, color3), 1)




cv2.imshow('paint5', paint5)
cv2.imshow('erosion', erosion)

# paint2 = cv2.merge([blank,acheck,paint2])   #bgr

test1 = np.ones((h,w),np.uint8)
cv2.imshow('edges2', edges2)
# cv2.imshow('edges3', edges3)
# cv2.imshow('paint3', paint3)
cv2.imshow('paint2', paint2)
cv2.imshow('origing1', g1)
cv2.imshow('origing0', img1)
cv2.imshow('paint4', paint4)


# cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area_erosion_contour.jpg', paint5)
# cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area_erosion.jpg', erosion)
# cv2.imwrite('papaya6_canny.jpg', edges2)
# # cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area_multicolor.jpg', paint2)
# cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area_erosion_contour_to_g1.jpg', g1)
# cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area_erosion_contour_to_img.jpg', img1)
# cv2.imwrite('papaya6_contour_frame_Hull_contour_corners_area.jpg', paint4)

# cv2.imshow('image4', test1)
# plt.imshow(test1, cmap='gray')
# plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()

