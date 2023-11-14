import rembg as rbg
import cv2
import numpy as np
from svgpathtools import svg2paths
import subprocess
import os
import matplotlib.pyplot as plt

MAX_RESOLUTION = 32767

def make_svg (img, basepath):
  cv2.imwrite(os.path.join(basepath, 'file.bmp'), img)
  subprocess.call(['./potrace/potrace.exe', '-s', os.path.join(basepath, 'file.bmp'), '-o', os.path.join(basepath, 'file.svg')])

def convert_paths_to_point_paths (paths):
  res = []
  for path in paths:
    sp = int(path.length(0, 1) / 50)
    point_path = list(map(lambda x: (np.real(path.point(x)), np.imag(path.point(x))), np.linspace(0, 1, sp)))
    res += [point_path]
  return res

def get_paths_bbox (paths):
  min_x, min_y, max_x, max_y = 1e+9, 1e+9, -1e9, -1e9
  for path in paths:
    xl, xr, yl, yr = path.bbox()
    min_x, min_y, max_x, max_y = min(min_x, xl), min(min_y, yl), max(max_x, xr), max(max_y, yr)
  return min_x, min_y, max_x, max_y

def offset_point_paths (point_paths, offset):
  res = []
  for point_path in point_paths:
    sub_res = []
    for point in point_path:
      sub_res += [(np.array(point) + np.array(offset)).tolist()]
    res += [sub_res]
  return res

def scale_point_paths (point_paths, scale):
  res = []
  for point_path in point_paths:
    res += [(np.array(point_path) * scale).tolist()]
  return res

def scatter_point_paths (point_paths):
  for point_path in point_paths:
    plt.scatter([point[0] for point in point_path], [point[1] for point in point_path], s=0.1, c='black')

def check_vertical (ratio, shape):
  return ratio >= shape[1] / shape[0]

def scale_point_paths_for_resolution (point_paths, bbox, shape, resolution):
  point_paths = offset_point_paths(point_paths, [-bbox[0], -bbox[1]])
  if check_vertical((bbox[3] - bbox[1]) / (bbox[2] - bbox[0]), shape):
    point_paths = scale_point_paths(point_paths, resolution / (bbox[3] - bbox[1]))
  else:
    point_paths = scale_point_paths(point_paths, resolution * (shape[0] / shape[1]) / (bbox[2] - bbox[0]))
  return point_paths

def cast_point_paths_to_int (point_paths):
  res = []
  for point_path in point_paths:
    sub_res = []
    for point in point_path:
      sub_res += [[int(point[0]), int(point[1])]]
    res += [sub_res]
  return res

def test_get_paths ():
  make_svg(cv2.imread('./file.png'), './generates')
  paths = svg2paths(os.path.join('./generates', 'file.svg'))[0]
  bbox = get_paths_bbox(paths)
  point_paths = convert_paths_to_point_paths(paths)
  point_paths = scale_point_paths_for_resolution(point_paths, bbox, [200, 287], MAX_RESOLUTION)
  point_paths = cast_point_paths_to_int(point_paths)
  scatter_point_paths(point_paths)
  print(point_paths)
  plt.autoscale()
  plt.axis('equal')
  plt.show()
