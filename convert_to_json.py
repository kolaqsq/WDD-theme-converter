"""
This script converts an XML metadata from extract_heic.py script to a json file for WDD and makes a .dww file
"""

import os
import shutil
import sys
from zipfile import ZipFile

from bs4 import BeautifulSoup as Soup

inp_dir = sys.argv[1]


def solar_convert(input_data, json):
    sunrise_img = []
    day_img = []
    sunset_img = []
    night_img = []
    input_data.seek(0, 0)

    for string in input_data:
        if string == 'a\n':
            altitude = float(input_data.readline())
            input_data.readline()
            index = int(input_data.readline())
            input_data.readline()
            azimuth = float(input_data.readline())

            if (azimuth <= 180) and (altitude <= 0):
                sunrise_img.append([azimuth, altitude, index])
            elif (azimuth <= 180) and (altitude > 0):
                day_img.append([azimuth, altitude, index])
            elif (azimuth > 180) and (altitude > 0):
                sunset_img.append([azimuth, altitude, index])
            elif (azimuth > 180) and (altitude <= 0):
                night_img.append([azimuth, altitude, index])

    i = 0
    json.write('\t"sunriseImageList": [\n')
    if sunrise_img:
        if len(sunrise_img) > 1:
            for i in range(len(sunrise_img) - 1):
                json.write('\t\t' + str(sunrise_img[i][2] + 1) + ',\n')
            json.write('\t\t' + str(sunrise_img[i + 1][2] + 1) + '\n')
        else:
            json.write('\t\t' + str(sunrise_img[0][2] + 1) + '\n')
    else:
        json.write('\t\t' + str(day_img[0][2] + 1) + ',\n')
    json.write('\t],\n')

    json.write('\t"dayImageList": [\n')
    if len(day_img) > 1:
        for i in range(len(day_img) - 1):
            json.write('\t\t' + str(day_img[i][2] + 1) + ',\n')
        json.write('\t\t' + str(day_img[i + 1][2] + 1) + '\n')
    else:
        json.write('\t\t' + str(day_img[0][2] + 1) + '\n')
    json.write('\t],\n')

    json.write('\t"sunsetImageList": [\n')
    if sunset_img:
        if len(sunset_img) > 1:
            for i in range(len(sunset_img) - 1):
                json.write('\t\t' + str(sunset_img[i][2] + 1) + ',\n')
            json.write('\t\t' + str(sunset_img[i + 1][2] + 1) + '\n')
        else:
            json.write('\t\t' + str(sunset_img[0][2] + 1) + '\n')
    else:
        json.write('\t\t' + str(night_img[0][2] + 1) + ',\n')
    json.write('\t],\n')

    json.write('\t"nightImageList": [\n')
    if len(night_img) > 1:
        for i in range(len(night_img) - 1):
            json.write('\t\t' + str(night_img[i][2] + 1) + ',\n')
        json.write('\t\t' + str(night_img[i + 1][2] + 1) + '\n')
    else:
        json.write('\t\t' + str(night_img[0][2] + 1) + '\n')
    json.write('\t]\n')

    return json


def h24_convert(input_data, json):
    sunrise_img = []
    day_img = []
    sunset_img = []
    night_img = []
    input_data.seek(0, 0)

    for string in input_data:
        if string == 'i\n':
            index = int(input_data.readline())
            input_data.readline()
            time = float(input_data.readline()) * 24

            if (time >= 6) and (time <= 8):
                sunrise_img.append([time, index])
            elif (time > 8) and (time < 19):
                day_img.append([time, index])
            elif (time >= 19) and (time <= 21):
                sunset_img.append([time, index])
            else:
                night_img.append([time, index])

    i = 0
    json.write('\t"sunriseImageList": [\n')
    if sunrise_img:
        if len(sunrise_img) > 1:
            for i in range(len(sunrise_img) - 1):
                json.write('\t\t' + str(sunrise_img[i][1] + 1) + ',\n')
            json.write('\t\t' + str(sunrise_img[i + 1][1] + 1) + '\n')
        else:
            json.write('\t\t' + str(sunrise_img[0][1] + 1) + '\n')
    else:
        json.write('\t\t' + str(day_img[0][1] + 1) + ',\n')
    json.write('\t],\n')

    json.write('\t"dayImageList": [\n')
    if len(day_img) > 1:
        for i in range(len(day_img) - 1):
            json.write('\t\t' + str(day_img[i][1] + 1) + ',\n')
        json.write('\t\t' + str(day_img[i + 1][1] + 1) + '\n')
    else:
        json.write('\t\t' + str(day_img[0][1] + 1) + '\n')
    json.write('\t],\n')

    json.write('\t"sunsetImageList": [\n')
    if sunset_img:
        if len(sunset_img) > 1:
            for i in range(len(sunset_img) - 1):
                json.write('\t\t' + str(sunset_img[i][1] + 1) + ',\n')
            json.write('\t\t' + str(sunset_img[i + 1][1] + 1) + '\n')
        else:
            json.write('\t\t' + str(sunset_img[0][1] + 1) + '\n')
    else:
        json.write('\t\t' + str(night_img[0][1] + 1) + ',\n')
    json.write('\t],\n')

    json.write('\t"nightImageList": [\n')
    if len(night_img) > 1:
        for i in range(len(night_img) - 1):
            json.write('\t\t' + str(night_img[i][1] + 1) + ',\n')
        json.write('\t\t' + str(night_img[i + 1][1] + 1) + '\n')
    else:
        json.write('\t\t' + str(night_img[0][1] + 1) + '\n')
    json.write('\t]\n')

    return json


if __name__ == "__main__":
    if not os.path.isdir(inp_dir + '_wdd'):
        shutil.copytree(inp_dir, inp_dir + '_wdd')

    inp = open(inp_dir + '_wdd/metadata.xml', mode='r')
    meta = Soup(inp.read(), features="lxml")
    out = open(inp_dir + '_wdd/' + inp_dir + '_wdd.json', mode='w')

    temp = open(inp_dir + '_wdd/temp.txt', mode='w+')
    temp.write(meta.get_text())
    temp.seek(0, 0)

    out.write('{\n'
              '\t"imagesZipUri": "' + inp_dir + '.ddw",\n'
              '\t"imageFilename": "' + os.path.basename(inp_dir).replace(' ', '_') + '_*.jpg",\n'
              '\t"imageCredits": "convert_to_json.py by kolaqsq",\n'
              '\t"displayName": "' + inp_dir + '",\n')

    for line in temp:
        if line.find('a\n') != -1:
            solar_convert(temp, out)
            break
        if line.find('t\n') != -1:
            h24_convert(temp, out)
            break

    out.write('}\n')

    inp.close()
    out.close()
    temp.close()

    os.remove(inp_dir + '_wdd/metadata.xml')
    os.remove(inp_dir + '_wdd/temp.txt')

    with ZipFile(inp_dir + '.ddw', 'w') as theme_file:
        for folderName, subfolders, filenames in os.walk(inp_dir + '_wdd'):
            for filename in filenames:
                theme_file.write(inp_dir + '_wdd/' + filename, filename)
