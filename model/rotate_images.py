from PIL import Image, ExifTags

'''
对于手机、相机等设备拍摄的照片，由于手持方向的不同，拍出来的照片可能是旋转0°、90°、180°和270°。即使在电脑上利用软件将其转正，他们的exif信息中还是会保留方位信息。
在用PIL读取这些图像时，读取的是原始数据，也就是说，即使电脑屏幕上显示是正常的照片，用PIL读进来后，也可能是旋转的图像，并且图片的size也可能与屏幕上的不一样。
--------------------- 
原文：https://blog.csdn.net/mizhenpeng/article/details/82794112 
'''
def rotate_image(file):
    img = Image.open(file)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand = True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand = True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand = True)
    except:
        pass
    img.save(file)


