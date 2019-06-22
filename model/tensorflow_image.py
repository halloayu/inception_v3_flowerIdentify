import tensorflow as tf
import matplotlib.pyplot as plt
from model.rotate_images import rotate_image

decode_jpeg_data = tf.placeholder(dtype=tf.string)
decode_jpeg = tf.image.decode_jpeg(decode_jpeg_data, channels=3)

def image_handler(file_path, restore_path):
    '''
    根据中心区域截取最大正方形，缩小成299x299
    :param file_path: 图片源地址
    :param restore_path: 缩小后的图片存储地址
    :return: none
    '''
    image_row_data = tf.gfile.FastGFile(file_path, 'rb').read()
    with tf.Session() as sess:
        # 计算截图图片的最大正方形的边长
        image = sess.run(decode_jpeg, feed_dict={decode_jpeg_data: image_row_data})
        width = image.shape[0]
        height = image.shape[1]
        clip_size = min(height, width) #取小的边
        # 图片解码
        image_data = tf.image.decode_jpeg(image_row_data)
        img_array = image_data.eval()  # 将tensor对象转成数组
        # 图片显示
        #plt.imshow(img_array)
        #plt.show()
        # 图片剪裁299x299
        clip_image = tf.image.resize_image_with_crop_or_pad(image_data, clip_size, clip_size)
        # 图片缩小(根据实际拍摄的图片来，我这里缩小6倍， 504x672)
        resize_image = tf.image.resize_images(clip_image, [299, 299], method=1)
        # 图像重编码
        image_data = tf.image.convert_image_dtype(resize_image, dtype=tf.uint8)
        encode_image = tf.image.encode_jpeg(image_data)
        # 6.图片保存
        with tf.gfile.GFile(restore_path, "wb") as f:
            f.write(encode_image.eval())

if __name__ == '__main__':
    i = 1
    while i < 101:
        j = str(i)
        file_path = "./FlowerLibrary/拍摄的三色堇/IMG_Pansy ("+j+").jpg"
        restore_path = "./flower_photos/Pansy/IMG_Pansy"+j+"-1.jpg"
        '''图片旋转处理'''
        rotate_image(file_path)
        image_handler(file_path, restore_path)
        i += 1
        if i % 10 == 0:
            print(i)