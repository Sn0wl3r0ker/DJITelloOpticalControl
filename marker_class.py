import numpy as np
#from plot3d import Plotting
from timeit import default_timer as timer
import time
import math
import transformations as tf
import cv2
import threading

# limit for averaging
ALLOW_LIMIT = 12

class Markers():
    def __init__(self, MARKER_SIDE, getCoords_event):
        # intiialise arrays
        self.ids = []
        self.tvec_origin = []
        self.rvec_origin = []
        self.dRot = []
        self.angle_origin = np.zeros((1,3))
        self.height_origin = 0

        # for filtering values
        self.allow_use = []
        self.tvec_max = []
        self.tvec_min = []

        # the first markers orientation
        self.orientation = np.zeros((2,3))

        # for logging
        self.OpenedFile=False

        self.getCoords_event = getCoords_event

    # Append marker to the list of stered markers
    def appendMarker(self, seen_id_list, tvec, rvec, angles, tof):
        for n_id in seen_id_list:
            n_index = seen_id_list.index(n_id)
            if n_id == 1 and len(self.ids) == 0:
                # not in self.ids and len(self.ids) == 0:
                self.ids.append(n_id)
                self.rvec_origin.append(rvec[n_index])
                self.dRot.append(np.array([[1,0,0],[0,1,0],[0,0,1]]))
                self.allow_use.append(ALLOW_LIMIT)
                self.tvec_max.append(0)
                self.tvec_min.append(10000)
                self.angle_origin = angles
                tvec_in_marker = tf.TranslationInMarker(rvec[n_index], tvec[n_index])
                self.height_origin = abs(tof) - tvec_in_marker[0][1]
                print(tof)
                print(tvec_in_marker)
                print(self.height_origin)
                self.tvec_origin.append(np.array([[0, self.height_origin, 0]]))
                # vertical orientation
                self.orientation = np.array([[1, -1, 1],[0, 2, 1]])
                print("Origin set")
            elif n_id not in self.ids and len(self.ids) > 0 and len(seen_id_list) >= 2:
                self.ids.append(n_id)
                self.tvec_origin.append(np.array([[0, 0, 0]]))
                self.rvec_origin.append(np.array([[0, 0, 0]]))
                self.dRot.append(np.array([[0,0,0],[0,0,0],[0,0,0]]))
                self.allow_use.append(0)
                self.tvec_max.append(0)
                self.tvec_min.append(10000)
                for m_id in seen_id_list:
                    if m_id in self.ids and m_id != n_id and self.allow_use[self.ids.index(m_id)]==ALLOW_LIMIT:
                        # n is to be added, m is already in list
                        m_index = seen_id_list.index(m_id)
                        m_index_list = self.ids.index(m_id)
                        n_index_list = self.ids.index(n_id)
                        t, R, r, a, ma, mi = tf.getTransformations(tvec[m_index], tvec[n_index], rvec[m_index], rvec[n_index],
                                                        self.tvec_origin[m_index_list], self.tvec_origin[n_index_list],
                                                        self.rvec_origin[m_index_list], self.rvec_origin[n_index_list],
                                                        self.dRot[m_index_list], self.dRot[n_index_list],
                                                        self.allow_use[n_index_list], ALLOW_LIMIT,
                                                        self.tvec_max[n_index_list], self.tvec_min[n_index_list])
                        self.tvec_origin[n_index_list] = t
                        self.dRot[n_index_list] = R
                        self.rvec_origin[n_index_list] = r
                        self.allow_use[n_index_list] = a
                        self.tvec_max[n_index_list] = ma
                        self.tvec_min[n_index_list] = mi
                        break
            elif n_id in self.ids and self.allow_use[self.ids.index(n_id)]<ALLOW_LIMIT:
                for m_id in seen_id_list:
                    if m_id in self.ids and m_id != n_id and self.allow_use[self.ids.index(m_id)]==ALLOW_LIMIT:
                        # n is to be added, m is already in list
                        m_index = seen_id_list.index(m_id)
                        m_index_list = self.ids.index(m_id)
                        n_index_list = self.ids.index(n_id)
                        t, R, r, a, ma, mi = tf.getTransformations(tvec[m_index], tvec[n_index], rvec[m_index], rvec[n_index],
                                                        self.tvec_origin[m_index_list], self.tvec_origin[n_index_list],
                                                        self.rvec_origin[m_index_list], self.rvec_origin[n_index_list],
                                                        self.dRot[m_index_list], self.dRot[n_index_list],
                                                        self.allow_use[n_index_list], ALLOW_LIMIT,
                                                        self.tvec_max[n_index_list], self.tvec_min[n_index_list])
                        self.tvec_origin[n_index_list] = t
                        self.dRot[n_index_list] = R
                        self.rvec_origin[n_index_list] = r
                        self.allow_use[n_index_list] = a
                        self.tvec_max[n_index_list] = ma
                        self.tvec_min[n_index_list] = mi
                        break

    # Calculate camera pose from seen markers
    def getCoords(self, seen_id_list, tvecs, rvecs, angles):
        length = len(seen_id_list)
        len_diff = 0
        dtv = np.zeros((1,3))
        drv = np.zeros((1,3))
        for i in range(length):
            if seen_id_list[i] in self.ids:
                ind = self.ids.index(seen_id_list[i])
                if self.allow_use[ind] == ALLOW_LIMIT:
                    dtv = dtv + tf.calculatePos(tvecs[i], rvecs[i], self.tvec_origin[ind], self.dRot[ind])
                else:
                    len_diff = len_diff + 1

        length = length - len_diff
        if length>0:
            dtv=dtv/length

        dtv[0][2] = self.height_origin + dtv[0][2]

        drv = angles - self.angle_origin

        #print(drv)
        #time.sleep(0.1)

        return dtv, drv
    
    # Check if ID already stored
    def ContainsIDs(self, seen_id_list):
        temp = False
        for ID in seen_id_list:
            if ID in self.ids:
                temp = True
        
        return temp

    # Reset the coordinate system
    def nullCoords(self):
        self.ids = []
        self.tvec_origin = []
        self.rvec_origin = []
        self.dRot = []
        self.allow_use = []
        self.tvec_max = []
        self.tvec_min = []
        self.orientation = np.zeros((2,3))
        self.angle_origin = np.zeros((1,3))
        self.height_origin = 0

    def getMov(self, seen_id_list, tvecs, rvecs, angles):
        if self.getCoords_event.is_set() and not self.OpenedFile:
            dtv, drv = self.getCoords(seen_id_list, tvecs, rvecs, angles)
            self.start=timer()
            self.t=[0]
            self.tvec_all=dtv
            self.rvec_all=drv
            self.OpenedFile=True
            print("Collecting data")
        elif self.getCoords_event.is_set() and self.OpenedFile:
            dtv, drv = self.getCoords(seen_id_list, tvecs, rvecs, angles)
            self.t=np.append(self.t,[timer()-self.start],axis=0)
            self.tvec_all=np.append(self.tvec_all,dtv,axis=0)
            self.rvec_all=np.append(self.rvec_all,drv,axis=0)
        elif not self.getCoords_event.is_set() and self.OpenedFile:
            timestr = time.strftime("%Y%m%d_%H%M%S")
            np.savez("results/movement_"+timestr, t=self.t, tvecs=self.tvec_all, rvecs=self.rvec_all,
                     t_origin=np.asarray(self.tvec_origin), r_origin=np.asarray(self.rvec_origin),
                     orientation=self.orientation)
            self.OpenedFile=False
            print("saved")
            #self.plotter.plotout("results/movement_"+timestr+".npz")