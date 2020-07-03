var tarpitHost = window.globalConfig.api;


var searchArr=[];
if(localStorage.search){
    searchArr = localStorage.search.split(',')
}else{
    searchArr = []
}
// console.log(searchArr)
MapSearchArr(searchArr);



function search() {
    //搜索点击按钮触发事件

    var key_word = $("#keyword").val().replace(/^\s+|\s+$/g, "");  // 搜索关键词. (去除两边空格)
    if(key_word === ""){
        layui.use('layer', function () {
            var layer = layui.layer;
            layer.msg("请输入搜索关键词.");
        });
        return false;
    }else{
        window.location.href = '/result/?keyword='+key_word+'&cur_page=1'

    }
    // if(key_word.length >2){
        killRepeat(key_word);
        localStorage.search = searchArr;
    // }




}

//回车键监听事件
// $("#keyword").bind("keyup", function(event) {
//
//     if (event.keyCode === "13") { //keyCode=13为回车键
//         alert(1)
//         search();
//     }
// });

document.onkeydown = function(e){
    if(e.keyCode === 13){
    	search();
    }
};




//搜索建议
$('#keyword').bind('input propertychange ',function () {
    var searchText = $(this).val();
    $.ajax({
        url: tarpitHost+"/api/suggest/?keyword="+searchText,
        type: "GET",
        async: false,
        contentType: false,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            //{"status":200,"response":"成功!"}
            $(".suggestion-list div").remove();
            if(json.status === 200){
                console.log(json.response)
                if(json.response.length !==0){
                    $(".suggestion-list").show();
                    $.each(json.response,function (i,value) {
                        var li = '<div class="suggest-li" onclick="suggest_click(this)"><a href="#">'+value+'</a></div>'
                        $(".suggestion-list").append($(li))

                    })
                }else{
                    $(".suggestion-list").hide();
                }
            }
        }
    })
})


// $('#keyword').blur(function () {
//     $("#search_button").css('color','white');
//     $("#suggestion-list .suggest-li").remove();
//     $("#suggestion-list ").css('display','none');
// })

function suggest_click(obj) {
    var value = $(obj).text();
    $("#keyword").val(value);
    search();
}


function killRepeat(val) {
    var kill = 0;
    for(var i=0;i<searchArr.length;i++){
        if(val===searchArr[i]){
            kill++;
        }
    }
    if(kill<1){
        searchArr.unshift(val);
    }else{
        removeByvalue(searchArr,val);
        searchArr.unshift(val);
    }
}

function removeByvalue(arr,val) {
    for(var i=0;i<arr.length;i++){
        if(arr[i] ===val){
            arr.splice(i,1);
            break;
        }
    }
}

function MapSearchArr(searchArr) {
    var tempHtml = "";
    var arrlen = 0;
    if(searchArr.length>5){
        arrlen = 5

    }else {
        arrlen = searchArr.length;
    }
    for(var i=0;i<arrlen;i++){
        tempHtml += '<a href="'+tarpitHost+'/result/?keyword='+searchArr[i]+'&cur_page=1'+'">'+searchArr[i]+'</a>';
    }
    $('#apps').append(tempHtml)
}



