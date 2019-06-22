import tensorflow as tf
import numpy as np
from model import train, data_process
from tensorflow.python.platform import gfile

# 训练好的inception-v3模型文件名
TRAIN_FILE = './model/train_dir/model.pb'
MODEL_FILE = './model/inceptionV3/tensorflow_inception_graph.pb'
OUTPUT_TENSOR_NAME = 'output/prob:0' # 新的瓶颈节点
bottleneck_input_name = 'BottleneckInputPlaceholder:0'
INPUT_DATA = './model/'+train.INPUT_DATA
BOTTLENECK_TENSOR_NAME = data_process.BOTTLENECK_TENSOR_NAME
JPEG_DATA_TENSOR_NAME = data_process.JPEG_DATA_TENSOR_NAME
# 测试数据
file_path = './static/images/target.jpg'

def get_image_value(file_name):
    # 加载模型
    with tf.Graph().as_default() as graph:
        with tf.Session().as_default() as sess:
            with tf.gfile.FastGFile(MODEL_FILE, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(graph_def, name='', return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])
            image_raw_data = gfile.FastGFile(file_name, 'rb').read()
            image_value = sess.run(bottleneck_tensor, {jpeg_data_tensor: image_raw_data})
            image_value = np.squeeze(image_value)
            images = []
            images.append(image_value)
    return images

def prediction(image_value):
    # 加载模型
    with tf.Graph().as_default() as graph:
        with tf.Session().as_default() as sess:
            with tf.gfile.FastGFile(TRAIN_FILE, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                final_tensor, bottleneck_input = tf.import_graph_def(graph_def, name='', return_elements=[OUTPUT_TENSOR_NAME, bottleneck_input_name])
            predictions = sess.run(final_tensor, {bottleneck_input: image_value})
            predictions = np.squeeze(predictions)
            flower_species = np.argmax(predictions) # 取预测最大值的索引为花朵种类(按花朵的训练顺序)
            return flower_species

def flower_identify():
    image_value = get_image_value(file_path)
    flower_species = prediction(image_value)
    # processed_data = np.load(INPUT_DATA)
    # labels = processed_data[6]
    # print(labels[flower_species])
    # return labels[flower_species]
    return flower_species
