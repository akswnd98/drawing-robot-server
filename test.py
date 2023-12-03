import utils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from svgpathtools import svg2paths2, document

if __name__ == '__main__':
  utils.test_get_paths()
  img = cv2.imread('./aaaaa.jpg')
  utils.make_svg_non_flask(img, '.')

  svg = svg2paths2('./file.svg')
  paths = svg[0]
  print(svg[2]['height'])
  print(utils.get_paths_bbox(paths))
  # for path in paths:
  #   sp = int(path.length(0, 1) / 50)
  #   xs = list(map(lambda x: np.real(path.point(x)), np.linspace(0, 1, sp)))
  #   ys = list(map(lambda y: np.imag(path.point(y)), np.linspace(0, 1, sp)))
  #   plt.scatter(xs, ys, s=1, c='black')
  # plt.autoscale()
  # plt.axis('equal')
  # plt.show()
