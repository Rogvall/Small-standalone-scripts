"""
This file reads in two .xyz-files and outputs a 3rd file with the atomic coordinates changed to a coordinate inbetween those in the two files.
Note: Add the file path for your files and change the code in 4 places for each new file (# change1, # change2, # change3, # change4).
Always check the result after. A visulaisation program for molecules can be used for that.

Description
Reading each line in the two xyz-atomic position files, finding all lines that have atomic coordinates in them (i.e. all lines with a dot in them).
Then a distance between "the same atom" in the two files is calculated and the new doordinate/distance is printed to a new xyz-file.

Note: This program only works in some circumstances, it can not be applied to two random .xyz-files
The program assumes that all rows containing "." is a row with atomic coordinates (e.g. pre info with crystal structure and such should be removed from the file), that the first column is the atom, and 2-4 column is the coordinates.
It also assumes a certain length of each coordinate and that the atoms are arrange in the same order (i.e. atom 4 in file is the "same" atom as atom 4 in file 2).
These assumptions are used because they are valid in my cases.

The file may contain errors. Use at own discretion.
"""


def coord_from_string(each_line):  # Picking out the x, y, z coordinate for the string "each_line".
    # Returns 3 coorddinates
    # Note the string have to have a specific setup (the first 3 points have to be decimal points for numbers that have 1-3 numbers before the decimal point and at most 14 after.
    x_position_min: int = each_line.find(".") - 3  # The first "." comes in the "x"-coordinate. I find the position of the first charracter (3 positions in front of the ".")
    x_position_max: int = x_position_min + 18  # The position of the last digit for the x-coordiante (18 positions behind of the first charracter)
    y_position_min: int = each_line.find(".",
                                         x_position_max) - 3  # The second ".", is the first "." after the "last" charracter of the x-coordinate
    y_position_max: int = y_position_min + 18
    z_position_min: int = each_line.find(".", y_position_max) - 3
    z_position_max: int = z_position_min + 18

    atom = str(each_line[0:3]).replace(" ", "") # Removes all possible empty spaces. Note! If the coordinates are not read in correctly this action will might merge two numbers into one, giving a wrong coordinate.
    x_coord = float(each_line[x_position_min:x_position_max])  # Converting the sting that consist of the charracter of the x-coordinate into a decimalnumber/float number.
    y_coord = float(each_line[y_position_min:y_position_max])
    z_coord = float(each_line[z_position_min:z_position_max])
    return atom, x_coord, y_coord, z_coord


# The start of the program
# Reads for 2 geometry xyz.files and creates a third.
read_file1 = open("filepath1", "r")  # opens the file as a variable called "read_file", or creates a readable "string" of my file... filepath should be changed to your file path e.g. C:\\Users\\TheSwede\\Desktop\\ChemistryIsAwesome\\Oxytocin.xyz
read_file2 = open("filepath2", "r")
write_file = open("filepath3", "w")  # change1 change the filename (e.g. FeCAB2_5-7_GS-short.xyz) each time you make a new file!
phrase1 = "."  # We only want rows with dots "." in them.
coord1 = []
coord2 = []
coord_new = []

# part one, make 2 lists (one from each input file) with all atomic coordinates in them...
for each_line in read_file1:  # A for-loop, "in" gives us each row in the "string"/file "read_file1". Each row is named/associated/saved in my variable "each_line"
    if each_line.find(phrase1) >= 0:  # "find" looks for the string "." and return the position in the string (a number between 0 and infinity), if it can't find "." it returns a negative number, so if "each_line.find(phrase)" is true we enter the if-statement
        atom, x_coord, y_coord, z_coord = coord_from_string(each_line)  # Reading in the x, y, z coordinate for each line.
        coord1.append([atom, x_coord, y_coord, z_coord])
read_file1.close()  # Closing the read_file, this is not necessary if we don't want to write to this file.

for each_line in read_file2:
    if each_line.find(phrase1) >= 0:
        atom, x_coord, y_coord, z_coord = coord_from_string(each_line)
        coord2.append([atom, x_coord, y_coord, z_coord])
read_file2.close()

write_file.write(str(63) + "\n") # Adding the header in mine .xyz-file
write_file.write(str(63) + "\n")

# Part 2, calculate the new coordinates between read_file1 and read_file2...
for i in range(len(coord1[:])):
    if coord1[i][0].find(coord2[i][0]) >= 0:
        coord_tempx = coord1[i][1] + (coord2[i][1] - coord1[i][1]) * 7 / 12  # change 2, change the 7/12 (i.e. the position of the new coordinate as a vector between the coordinate in file 1 towards file2).
        coord_tempy = coord1[i][2] + (coord2[i][2] - coord1[i][2]) * 7 / 12  # change 3
        coord_tempz = coord1[i][3] + (coord2[i][3] - coord1[i][3]) * 7 / 12  # change 4 (change 2-4 to the same value).

    write_file.write(str(coord1[i][0]) + "        " + str(coord_tempx) + "        " + str(coord_tempy) + "        " + str(coord_tempz) + "\n")  # Writes the new coordinates to a file

write_file.close()  # Closing the write_file, this is not necessary if we don't try to ddo something stupid to this file, like writing more stuff or writing over the results.
print("Done, have a nice day! Greating from Jojo!")  # Notifys us that the program is done.... =)
