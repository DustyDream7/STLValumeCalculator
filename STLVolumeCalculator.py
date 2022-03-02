#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import struct
import sys
import os

class STLUtils:
    def resetVariables(self):
        self.normals = []
        self.points = []
        self.triangles = []
        self.bytecount = []
        self.fb = []  # debug

    # based on: http://stackoverflow.com/questions/1406029/how-to-calculate-the-volume-of-a-3d-mesh-object-the-surface-of-which-is-made-up
    def signedVolumeOfTriangle(self, p1, p2, p3):
        v321 = p3[0] * p2[1] * p1[2]
        v231 = p2[0] * p3[1] * p1[2]
        v312 = p3[0] * p1[1] * p2[2]
        v132 = p1[0] * p3[1] * p2[2]
        v213 = p2[0] * p1[1] * p3[2]
        v123 = p1[0] * p2[1] * p3[2]
        return (1.0 / 6.0) * (-v321 + v231 + v312 - v132 - v213 + v123)

    def unpack(self, sig, l):
        s = self.f.read(l)
        self.fb.append(s)
        return struct.unpack(sig, s)

    def read_triangle(self):
        n = self.unpack("<3f", 12)
        p1 = self.unpack("<3f", 12)
        p2 = self.unpack("<3f", 12)
        p3 = self.unpack("<3f", 12)
        b = self.unpack("<h", 2)
        self.normals.append(n)
        l = len(self.points)
        self.points.append(p1)
        self.points.append(p2)
        self.points.append(p3)
        self.triangles.append((l, l + 1, l + 2))
        self.bytecount.append(b[0])
        return self.signedVolumeOfTriangle(p1, p2, p3)

    def read_length(self):
        length = struct.unpack("@i", self.f.read(4))
        return length[0]

    def read_header(self):
        self.f.seek(self.f.tell() + 80)

    def cm3_To_inch3Transform(self, v):
        return v * 0.0610237441

    def calculateMassCM3(self, totalVolume):
        totalMass = (totalVolume * 1.04)
        return totalMass

    def calculateVolume(self, infilename, unit):
        print(infilename)
        self.resetVariables()
        totalVolume = 0
        totalMass = 0
        try:
            self.f = open(infilename, "rb")
            self.read_header()
            l = self.read_length()
            try:
                while True:
                    totalVolume += self.read_triangle()
            except Exception as e:
                 print(totalVolume)
            totalMass = self.calculateMassCM3(totalVolume)
        except Exception as e:
            print(e)
        return totalVolume

if __name__ == '__main__':
        mySTLUtils = STLUtils()
        with open('res.csv', 'w',encoding='gbk') as f:
            f.write("文件名" + "," + "体积(单位：mm^3)" + "\n")
            for name in [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1]=='.STL' or os.path.splitext(x)[1]=='.stl' or os.path.splitext(x)[1]=='.Stl')]:
                totalVolume = mySTLUtils.calculateVolume(name, "mm")
                f.write(name + "," + str(totalVolume) + "\n")