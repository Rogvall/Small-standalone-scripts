#!/bin/env python
from matplotlib import pyplot as plt
import math
import array as arr
import h5py

# This code transforms a diffraction pattern from a flat detector to the  the Ewaldssphere and then it rotates
# the diffraction patterns according to a unit quaternion. Then it plots one onr several diffraction patterns
# in the same plot so one can see how the diffraction patterns can fill up the Ewald sphere.
# Note: A lot of the comments are in swedish, they might be translated to english later.

# OBBS kolla att valet av quaternion för rotationen är korrekt, jag tror att motsatt rotation/quaternion ska användas
# (complex konjugaten av det som använts i Condor, i min fil har jag sparat komplexkonjugaten av condors rotationer) för att ge diffraktionsmänstrets korrekta orientering.
# Det går säkert att ta bort "genomskinligheten i plotten med något py-plot argument om man inte gillar att det är genomskinligt.
# Koden antar att filen med alla diffraktionsmönster är en h5py fil som innehåller diffraktionsmönsterna i en array av
# typen Intensitet = (N, x, y) och quaternionerna (komplexkonjugatet till den quaternion som angetts i Condor) i stilen a, b, c, d = (N, 4)
# Koden antar även att pixelstorleken på diffraktionsmänsterna är 110*8 mikrometer och att varje mänster består av
# 128*128 pixlar (och att mitten-pixeln är vid 64-pixlar)... Om detta inte är fallet så behöer det justeras i varje
# "huvudfoorloop". Det är 1 huvudfoor-lopp per diffraktionsmönster som man vill plotta.


# The function #rot_quaternion" takes in a position in real space (x,y,z) and rotates it according to the quaternion (a,bi,cj,dk), and returns the
# new coordinates of the rotated point in real space (I=x-direction, J=y-direction and K=z direction).
# a, bb, c, d are the quaternion values and x, y, z the coordinate of the point that should be rotated.
def rot_quaternion(a, b, c, d, x, y, z):
    I = (a * a + b * b - c * c - d * d) * x + 2 * (a * c * z - a * d * y + b * c * y + b * d * z)
    J = (a * a - b * b + c * c - d * d) * y + 2 * (-a * b * z + a * d * x + b * c * x + c * d * z)
    K = (a * a - b * b - c * c + d * d) * z + 2 * (a * b * y - a * c * x + b * d * x + c * d * y)
    return I, J, K

# Definierar arrayyerna med diffraktionsmönsterna som sen plottas.
condor2_x10 = arr.array("f", [])
condor2_y10 = arr.array("f", [])
condor2_z10 = arr.array("f", [])
condor2_intensity10 = arr.array("f", [])
dd = 0.13  # Detektoravståndet för Ewalssfärs-beräkningen.
lambda_1 = 1.5498e-10  # Våglängden på det inkommande ljuset för Ewaldssfärsberäkningen.

# Change "Path-file" to the path and filename for your file in your computer. Ex "home/myfolder/my_diffractionpattern_and_quaternion_file.h5"
with h5py.File("Path-file", 'r') as row:
    condor2 = row["patterns"][...]
    quaternion = row["extrinsic_quaternion"][...]


# För varje foor-loop ska man ändra/ange värdet på vilket diffraktionsmönster i listan över diffraktionsmänster som
# man använder. I den första looopen är det "90" som man ska ändra på för att välja ett specifikt diffraktionsmönster och dess quaternion.
# "90" ska ändras på 6 platser per huvud foor-loop (4 ggr i vridningen med quaternionen och 2 ggr för intensiteten i diffraktionsmönstret).
for i in range(128):
    for j in range(128):
        # Transformerar varje diffraktionsmönser så som det skulle se ut på Ewaldsfären
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1/lambda_1
        I, J, K = rot_quaternion(quaternion[90, 0], quaternion[90, 1], quaternion[90, 2], quaternion[90, 3],  # Roterar varje mönster på Ewaldsfären med quaternionen från condor-filen
                                 xx, yy, zz)  # Quaternion calculation, using that i
        # and j gives the position on the detector screen. The detector screen is 128=2*64 pixels long and each
        # pixel is 110 micro meter.

        # If the diffractions patterns are put into different variables/lists then they don't seem to intersect arpund (0,0,0), because of how python plots them. So all data have to be in the same variable/list.

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:  # Innan transformationen till Ewaldsfären och rotationen så var
            # diffaktogrammen i x (i) och y (j) led. Så vi sätter värdet på pixeln som är på "kanten" av diffraktogrammet till 5*10^-7 för att få en lagom mörk färg. Lägre färg = mörkare färg, högre färg = mer gul/grön färg.
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[90, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[90, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity
#            condor2_intensity10.append(math.log(1e-10))
#"""
#"""
for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[105, 0], quaternion[105, 1], quaternion[105, 2], quaternion[105, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[105, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[105, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

#"""
"""
# massa fler foor-loopar för att plotta mpna diffraktionsmönster ihop...
for i in range(128):
    for j in range(128):
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1
        I, J, K = rot_quaternion(quaternion[107, 0], quaternion[107, 1], quaternion[107, 2], quaternion[107, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i
        # and j gives the position on the detector screen. The detector screen is 128=2*64 pixels long and each
        # pixel is 110 micro meter.

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[107, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[107, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[10, 0], quaternion[10, 1], quaternion[10, 2], quaternion[10, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[10, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[10, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[24, 0], quaternion[24, 1], quaternion[24, 2], quaternion[24, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[24, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[24, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[120, 0], quaternion[120, 1], quaternion[120, 2], quaternion[120, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[120, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[120, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[13, 0], quaternion[13, 1], quaternion[13, 2], quaternion[13, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[13, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[13, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[140, 0], quaternion[140, 1], quaternion[140, 2], quaternion[140, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[140, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[140, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[35, 0], quaternion[35, 1], quaternion[35, 2], quaternion[35, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[35, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[35, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[16, 0], quaternion[16, 1], quaternion[16, 2], quaternion[16, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[16, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[16, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity


for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[170, 0], quaternion[170, 1], quaternion[170, 2], quaternion[170, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[170, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[170, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[57, 0], quaternion[57, 1], quaternion[57, 2], quaternion[57, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[57, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[57, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

for i in range(128):
    for j in range(128): # 106
        theta = math.pi / 2 - math.atan((i - 64) * (110e-6 * 8) / dd)
        phi = math.pi / 2 - math.atan((j - 64) * (110e-6 * 8) / dd)
        xx = 1 / lambda_1 * math.cos(phi) * math.sin(theta)
        yy = 1 / lambda_1 * math.cos(theta)
        zz = 1 / lambda_1 * math.sin(phi) * math.sin(theta) - 1 / lambda_1

        I, J, K = rot_quaternion(quaternion[37, 0], quaternion[37, 1], quaternion[37, 2], quaternion[37, 3],
                                 xx, yy, zz)  # Quaternion calculation, using that i

        condor2_x10.append(I)  # x-värde
        condor2_y10.append(J)  # y-värde
        condor2_z10.append(K)  # z-värde
        if i == 0 or i == 127 or j == 0 or j == 127:
            condor2_intensity10.append(math.log(5e-7))  # intenistet-värde # Note, change to a resonable value based on intensity
        elif condor2[37, i, j] > 0:
            #            print(condor2[10, i, j])
            condor2_intensity10.append(math.log(condor2[37, i, j]))  # intenistet-värde
        else:
            condor2_intensity10.append(math.log(5e-7))  # Note, change to a resonable value based on intensity

#"""
# Plots the "correctly rotated" 2Ddiffraction-slice from the condor-silmulation
# The plot can be twisted/rotated in the plot window to find a nice orientation of the diffraction patterns.
figN = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xs=condor2_x10, ys=condor2_y10, zs=condor2_z10, c=condor2_intensity10, s=1)
ax.axis('off')
plt.tight_layout()

plt.show()