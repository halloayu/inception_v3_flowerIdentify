# -*- coding: utf-8 -*-
# @File  :fi_handlers.py
# @Author:ZengYu
# @Date  :2019/5/16
# @software:PyCharm

import tornado.web
import tornado.websocket
from PIL import Image
import base64
from model.flower_identify import flower_identify

class FlowersInfo():
    flowersInfo = ["月季花(学名:Rosa chinensis Jacq.): 被称为花中皇后，又称“月月红”，是常绿、半常绿低矮灌木，四季开花，一般为红色，或粉色、偶有白色和黄色，可作为观赏植物，也可作为药用植物，亦称月季。有三个自然变种，现代月季花型多样，有单瓣和重瓣，还有高心卷边等优美花型；其色彩艳丽、丰富，不仅有红、粉黄、白等单色，还有混色、银边等品种；多数品种有芳香。月季的品种繁多，世界上已有近万种，中国也有千种以上。",
                   "绣球（学名：Hydrangea macrophylla (Thunb.) Ser. ）： 为虎耳草科绣球属植物。灌木，高1-4米；茎常于基部发出多数放射枝而形成一圆形灌丛；枝圆柱形。叶纸质或近革质，倒卵形或阔椭圆形。伞房状聚伞花序近球形，直径8-20厘米，具短的总花梗，花密集，粉红色、淡蓝色或白色；花瓣长圆形，长3-3.5毫米。蒴果未成熟，长陀螺状；种子未熟。花期6-8月。",
                   "万寿菊（Tagetes erecta L）为菊科万寿菊属一年生草本植物，茎直立，粗壮，具纵细条棱，分枝向上平展。叶羽状分裂；沿叶缘有少数腺体。头状花序单生；总苞杯状，顶端具齿尖；舌状花黄色或暗橙色；管状花花冠黄色。瘦果线形，基部缩小，黑色或褐色，被短微毛；冠毛有1-2个长芒和2-3个短而钝的鳞片。花期7-9月。",
                   "三色堇（学名：Viola tricolor L.）是堇菜科堇菜属的二年或多年生草本植物。基生叶叶片长卵形或披针形，具长柄，茎生叶叶片卵形、长圆形或长圆披针形，先端圆或钝，边缘具稀疏的圆齿或钝锯齿。三色堇是欧洲常见的野花物种，也常栽培于公园中，是冰岛、波兰的国花。花朵通常每花有紫、白、黄三色，故名三色堇。该物种较耐寒，喜凉爽，开花受光照影响较大。",
                   "石榴花，落叶灌木或小乔木石榴的花；为石榴属植物，石榴树干灰褐色，有片状剥落，嫩枝黄绿光滑，常呈四棱形，枝端多为刺状，无顶芽。石榴花单叶对生或簇生，矩圆形或倒卵形，新叶嫩绿或古铜色。花朵至数朵生于枝顶或叶腋，花萼钟形，肉质，先端6裂，表面光滑具腊质，橙红色，宿存。花瓣5～7枚红色或白色，单瓣或重瓣。"]

class FlowerIdentify(tornado.web.RequestHandler):
    def get(self):
        self.render("flower_identify.html")

class IdentifyHandler(tornado.websocket.WebSocketHandler):
    def post(self):
        # 从JSON字符串读取图片数据
        dataUrl = self.get_body_argument("image")
        Orientation = self.get_body_argument("orientation")  # 得到图片方向以便旋转处理
        content = base64.b64decode(dataUrl)
        '''保存到图片target.jpg'''
        file = open('./static/images/target.jpg', 'wb')
        file.write(content)
        file.close()

        '''图片旋转270(根据实际情况)'''
        img = Image.open('./static/images/target.jpg')
        if Orientation == "3":
            img = img.rotate(180, expand=True)
        elif Orientation == "6":
            img = img.rotate(270, expand=True)
        elif Orientation == "8":
            img = img.rotate(90, expand=True)
        img.save('./static/images/target.jpg')

        '''调用函数识别'''
        flowerIndex = flower_identify()  # 调用识别函数
        flowerInfo  = FlowersInfo.flowersInfo[flowerIndex]  # 得到结果，并从FlowersInfo里找到该花的资料
        self.render("fi_result.html", data=flowerInfo)
