import utils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from svgpathtools import svg2paths, document

if __name__ == '__main__':
  utils.test_get_paths()
  # img = cv2.imread('.\\file.png')
  # utils.make_svg(img, '.')

  # svg = svg2paths('.\\file.svg')
  # paths = svg[0]
  # for path in paths:
  #   sp = int(path.length(0, 1) / 50)
  #   xs = list(map(lambda x: np.real(path.point(x)), np.linspace(0, 1, sp)))
  #   ys = list(map(lambda y: np.imag(path.point(y)), np.linspace(0, 1, sp)))
  #   plt.scatter(xs, ys, s=1, c='black')
  # plt.autoscale()
  # plt.axis('equal')
  # plt.show()
