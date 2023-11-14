from flask import Flask, request
from flask_cors import CORS
import utils
import cv2
from werkzeug.utils import secure_filename
import os
from svgpathtools import svg2paths
from svgpathtools.path import CubicBezier, Line
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/get-paths', methods=['POST'])
def get_paths ():
  file = request.files['file']
  filename = secure_filename(file.filename)
  filepath = os.path.join('.\\uploads', 'file{}'.format(os.path.splitext(filename)[-1]))
  file.save(filepath)
  utils.make_svg(cv2.imread(filepath), '.\\generates')
  paths = svg2paths(os.path.join('.\\generates', 'file.svg'))[0]
  bbox = utils.get_paths_bbox(paths)
  point_paths = utils.convert_paths_to_point_paths(paths)
  # point_paths = utils.scale_point_paths_for_resolution(point_paths, bbox, [200, 287], utils.MAX_RESOLUTION)
  # point_paths = utils.cast_point_paths_to_int(point_paths)

  return {
    'pointPaths': point_paths,
    'bbox': bbox
  }

if __name__ == '__main__':
  load_dotenv()
  CORS(app)
  app.run(host=os.getenv('HOST'), port=int(os.getenv('PORT')))
