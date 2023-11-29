import utils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from svgpathtools import svg2paths, document
import os

utils.make_svg_non_flask(cv2.imread('./file.png'), './generates')
paths = svg2paths(os.path.join('./generates', 'file.svg'))[0]
bbox = utils.get_paths_bbox(paths)
point_paths = utils.convert_paths_to_point_paths(paths)


