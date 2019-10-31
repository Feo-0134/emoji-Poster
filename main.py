#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:28:51 2019

@author: junchengzhu
"""
from __future__ import division
import dlib                     #人脸识别的库dlib
import numpy as np              #数据处理的库numpy
import cv2                      #图像处理的库OpenCv
from skimage import io          #>pip install scikit-image,scipy

class face_emotion():
    def __init__(self):
        # 使用特征提取器get_frontal_face_detector
        self.detector = dlib.get_frontal_face_detector()
        # dlib的68点模型，使用作者训练好的特征预测器
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    def learning_face(self):
        # 眉毛直线拟合数据缓冲
        line_brow_x = []
        line_brow_y = []
        im_rd = cv2.imread("pic.png")
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
        faces = self.detector(img_gray, 0) # 检测到的人脸数
        # 待会要显示在屏幕上的字体
        font = cv2.FONT_HERSHEY_SIMPLEX
        if(len(faces)!=0):
            # 对每个人脸都标出68个特征点
            for k, d in enumerate(faces):
                cv2.rectangle(im_rd, (d.left(), d.top()),
                              (d.right(), d.bottom()), (0, 0, 255))
                cv2.rectangle(im_rd, (d.left()-10, d.top()-10),
                              (d.right()+10, d.bottom()+10), (0, 255, 0))
                # 用红色矩形框出人脸
                cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                # 计算人脸热别框边长
                self.face_width = d.right() - d.left()
                # 使用预测器得到68点数据的坐标
                shape = self.predictor(im_rd, d)
                # 圆圈显示每个特征点
                for i in range(68):
                    cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                    #cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y),
                    #            cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255, 255, 255))   
                # 分析任意n点的位置关系来作为表情识别的依据
                mouth_width = (shape.part(54).x - shape.part(48).x) / self.face_width  # 嘴巴咧开程度
                mouth_higth = (shape.part(66).y - shape.part(62).y) / self.face_width  # 嘴巴张开程度
                # print("嘴巴宽度与识别框宽度之比：",mouth_width_arv)
                # print("嘴巴高度与识别框高度之比：",mouth_higth_arv)
                # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                brow_sum = 0  # 高度之和
                frown_sum = 0  # 两边眉毛距离之和
                for j in range(17, 21):
                    brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                    frown_sum += shape.part(j + 5).x - shape.part(j).x
                    line_brow_x.append(shape.part(j).x)
                    line_brow_y.append(shape.part(j).y)
                # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                tempx = np.array(line_brow_x)
                tempy = np.array(line_brow_y)
                z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                self.brow_k = -round(z1[0], 3)  # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的
                brow_hight = (brow_sum / 10) / self.face_width  # 眉毛高度占比
                brow_width = (frown_sum / 5) / self.face_width  # 眉毛距离占比
                # print("眉毛高度与识别框高度之比：",round(brow_arv/self.face_width,3))
                # print("眉毛间距与识别框高度之比：",round(frown_arv/self.face_width,3))
                # 眼睛睁开程度
                eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                           shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)

                eye_hight = (eye_sum / 4) / self.face_width
                # print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))
                # 分情况讨论
                # 张嘴，可能是开心或者惊讶
                if round(mouth_higth >= 0.03):
                    if eye_hight >= 0.056:
                        print 'amazing-->[mouth_higth:{mouth_higth},eye_hight:{eye_hight},self.brow_k:{self.brow_k}]'
                        cv2.imwrite("amazing"+".png", im_rd)
                        cv2.putText(im_rd, "amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)
                    else:
                        print 'happy-->[mouth_higth:{mouth_higth},eye_hight:{eye_hight},self.brow_k:{self.brow_k}]'
                        cv2.imwrite("happy"+".png", im_rd)
                        cv2.putText(im_rd, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                                (0, 0, 255), 2, 4)
                # 没有张嘴，可能是正常和生气
                else:
                    if self.brow_k <= -0.2:# modify 0.3 as 0.2 by Andy
                        print 'angry-->[mouth_higth:{mouth_higth},eye_hight:{eye_hight},self.brow_k:{self.brow_k}]'
                        cv2.imwrite("angry"+".png", im_rd)
                        cv2.putText(im_rd, "angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255), 2, 4)
                    else:
                        print 'nature-->[mouth_higth:{mouth_higth},eye_hight:{eye_hight},self.brow_k:{self.brow_k}]'
                        cv2.imwrite("nature"+".png", im_rd)
                        cv2.putText(im_rd, "nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)
            # 标出人脸数
            cv2.putText(im_rd, "Faces: "+str(len(faces)), (20,50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # 没有检测到人脸
            cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        # 窗口显示
        # cv2.imshow("camera", im_rd)
        # cv2.imwrite("result"+".png", im_rd)
if __name__ == "__main__":
    my_face = face_emotion()
    my_face.learning_face()
