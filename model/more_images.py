import tensorflow as tf
import matplotlib.pyplot as plt
def encode_image(imageObj):
    image_data = tf.image.convert_image_dtype(imageObj, dtype=tf.uint8)
    encode_image = tf.image.encode_jpeg(image_data)
    return encode_image

def more_images(ori_file_path):

    file_path = ori_file_path + "1.jpg" #源图片地址
    up_down_image_path = ori_file_path + "2.jpg" #上下反转后的地址
    left_right_image_path = ori_file_path + "3.jpg" #左右反转后的地址
    diagonal_image_path = ori_file_path + "4.jpg" #对角线反转后的地址
    fifth_image_path = ori_file_path + "5.jpg" #随机调整色相饱和度后的地址
    image_row_data = tf.gfile.FastGFile(file_path, 'rb').read()
    with tf.Session() as sess:
        # 图片解码
        image_data = tf.image.decode_jpeg(image_row_data)
        # 图片处理以获得更多的图片
        up_down_image       = tf.image.flip_up_down(image_data)        # 上下反转
        left_right_image    = tf.image.flip_left_right(image_data)     # 左右反转
        diagonal_image      = tf.image.transpose_image(image_data)     # 对角线反转
        brightness_random   = tf.image.random_brightness(image_data, max_delta=0.3)  # 随机调整亮度，亮度在[-max_delta, +max_delta]]
        adjust_hue_image    = tf.image.adjust_hue(brightness_random, delta=0.08) # 色相随机
        fifth_image         = tf.image.random_saturation(adjust_hue_image, lower=0.5, upper=1.5) # 饱和度随机

        # 上下反转后的图片存储
        up_down_image = encode_image(up_down_image)
        with tf.gfile.GFile(up_down_image_path, "wb") as f:
            f.write(up_down_image.eval())
        # 左右反转后的图片存储
        left_right_image = encode_image(left_right_image)
        with tf.gfile.GFile(left_right_image_path, "wb") as f:
            f.write(left_right_image.eval())
        # 对角线反转后的图片存储
        diagonal_image = encode_image(diagonal_image)
        with tf.gfile.GFile(diagonal_image_path, "wb") as f:
            f.write(diagonal_image.eval())
        # 对角线反转后的图片存储
        fifth_image = encode_image(fifth_image)
        with tf.gfile.GFile(fifth_image_path, "wb") as f:
            f.write(fifth_image.eval())

if __name__ == '__main__':
    i = 1
    while (i < 101):
        j = str(i)
        ori_file_path = "./flower_photos/Pansy/IMG_Pansy" + j +"-"
        more_images(ori_file_path)
        i += 1
