from GaitCore.Core import Point


frames = {}
frames["stairA"] = [Point.Point(0, 0, 0),
                    Point.Point(63, 0, 0),
                    Point.Point(0, 42, 0),
                    Point.Point(63, 49, 0)]

frames["stairB"] = [Point.Point(0, 0, 0),
                    Point.Point(49, 0, 0),
                    Point.Point(28, 56, 0),
                    Point.Point(70, 70, 0)]

file00 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_00/subject_00_stair_config1_00.csv"
file01 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_01/subject_01_stair_config1_03.csv"
file02 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_02/subject_02_stair_config1_04.csv"
file03 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_03/subject_03_stair_config0_02.csv"
file04 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_04/subject_04_stair_config1_02.csv"
file05 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_05/subject_05_stair_config1_01.csv"
file06 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_06/subject_06_stair_config1_02.csv"
file07 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_07/subject_07_stair_config1_02.csv"
file08 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_08/subject_08_stair_config2_02.csv"
file09 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_09/subject_09_stair_config1_00.csv"
file10 = "/home/csbales/AIM_GaitData/Gaiting_stairs/subject_10/subject_10_stair_config1_00.csv"

files = [file00, file01, file02, file03, file05, file07, file09, file10]
sides = ["R", "R", "R", "R", "R", "R", "R", "R"]
