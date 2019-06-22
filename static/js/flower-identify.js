//对象获取
var take_picture = document.getElementById("take-picture");
var msg          = document.getElementById("message");   //提示信息
var fi_result    = document.getElementById("fi-result"); //识别结果
var canvas       = document.getElementById("canvas");
var ctx          = canvas.getContext("2d");
var canvas2      = document.getElementById("canvas2");
var ctx2         = canvas2.getContext("2d");
var userTemplateId = parent.window.templateId;
var pic;
var dataUrl ;
//判断浏览器是否支持FileReader接口
if (typeof FileReader == 'undefined') {
    msg.innerHTML = "当前浏览器无法支持FileReader接口,请更换主流浏览器!";
    //使选择控件不可操作
    take_picture.setAttribute("disabled", "disabled");
}
//图片缩小放在临时的canvas2里,然后截图中心区域传给后端
if (take_picture) {
    // 获得图片文件的引用
    take_picture.onchange = function (event) {
        var files = event.target.files, file;
        if (files && files.length > 0) {
            // 获取目前上传的文件
            file = files[0];
            console.log(file);
            //检查是否为图片
            if (!/image\/\w+/.test(file.type)) {
                alert("看清楚,这个需要图片！");
                return false;
            }
            //获取照片方向角属性，用户旋转控制
            EXIF.getData(file, function() {
                //alert(EXIF.pretty(this));
                EXIF.getAllTags(this);
                Orientation = EXIF.getTag(this, 'Orientation');
            });

            var fileReader = new FileReader();
            fileReader.onload = function (event) {
                var image    = new Image();
                image.src    = event.target.result;
                image.onload = function() {
                    canvas2.width  = 299;
                    canvas2.height = 299;
                    var height = this.naturalWidth/10;
                    var width = this.naturalHeight/10;
                    ctx2.drawImage(this, 0, 0, height, width); //把图片缩小10倍
                    saveUserTemplateAsImageData(Orientation);
                };
            };
        };
        fileReader.readAsDataURL(file);
    }
};
//对图片旋转处理
function rotateImg(img, direction) {
    //最小与最大旋转方向，图片旋转4次后回到原方向
    var min_step = 0;
    var max_step = 3;
    width  = canvas.width;
    height = canvas.height;
    if (img == null)return;
    var step = 2;
    if (step == null) {
        step = min_step;
    }
    if (direction == 'right') {
        step++;
        //旋转到原位置，即超过最大值
        step > max_step && (step = min_step);
    } else {
        step--;
        step < min_step && (step = max_step);
    }

    //旋转角度以弧度值为参数
    var degree = step * 90 * Math.PI / 180;
        switch (step) {
          case 0:
            ctx.drawImage(img, 0, 0);
            break;
          case 1:
            ctx.clearRect(0,0,299,299); //清空画布
            ctx.rotate(degree);
            ctx.drawImage(img, 0, -height);
            break;
          case 2:
            ctx.rotate(degree);
            ctx.drawImage(img, -width, -height);
            break;
          case 3:
            ctx.rotate(degree);
            ctx.drawImage(img, -width, 0);
            break;
        }
}

function saveUserTemplateAsImageData(Orientation){
    var dataUrl = canvas2.toDataURL("image/jpeg");
    ctx2.clearRect(0,0,299,299); //清空画布
    // 图片旋转，写入canvas
    var newImg = new Image();
    newImg.src = dataUrl;
    newImg.onload = function() {
        if(Orientation != "" && Orientation != 1){
            switch(Orientation){
                case 6://需要顺时针（向左）90度旋转
                    //alert('需要顺时针（向左）90度旋转');
                    rotateImg(this,'left');
                    break;
                case 8://需要逆时针（向右）90度旋转
                    //alert('需要顺时针（向右）90度旋转');
                    rotateImg(this,'right');
                    break;
                case 3://需要180度旋转
                    //alert('需要180度旋转');
                    rotateImg(this,'right');//转两次
                    rotateImg(this,'right');
                    break;
            }
        }
    };
    //向后端传递formData格式
    var imageDataB64 = dataUrl.substring(23); //去掉前22位
    var formData = new FormData();
    formData.set('image',imageDataB64);
    formData.set('orientation',Orientation);
    $.ajax({
        url: "/imgPost",
        method: "POST",
        data: formData,
        contentType: false, //不设置内容类型
        processData: false, //不处理数据
        success: function (data) {
            alert(data);
            $("#fi-result").html(data);
        },
        error: function (error) {
            alert("服务器连接失败!");
        }
    });
}
