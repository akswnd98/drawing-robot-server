from flask import Flask, request
from flask_cors import CORS
import utils
import cv2
from werkzeug.utils import secure_filename
import os
from svgpathtools import svg2paths2
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
  filepath = os.path.join('./uploads', 'file{}'.format(os.path.splitext(filename)[-1]))
  file.save(filepath)
  utils.make_svg(cv2.imread(filepath), './generates')
  paths, _, opt = svg2paths2(os.path.join('./generates', 'file.svg'))
  bbox = utils.get_paths_bbox(paths)
  point_paths = utils.convert_paths_to_point_paths(paths)
  point_paths = utils.flip_vertically_point_paths(point_paths)
  point_paths = utils.offset_point_paths(point_paths, np.array([0, float(opt['height'][0: -2]) * 10], dtype=np.float64))

  return {
    'pointPaths': point_paths,
    'bbox': bbox
  }

if __name__ == '__main__':
  load_dotenv()
  CORS(app)
  app.run(host=os.getenv('HOST'), port=int(os.getenv('PORT')))
