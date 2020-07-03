// 后台的URL
var url = window.globalConfig.api;


$(function () {
    // 用户登录:监听用户登录的状态,登录信息保存在session中.
    var user_token = window.sessionStorage.getItem("user_token");
    var img_token =window.sessionStorage.getItem("img_token");
    if (user_token !== null){
        // 如果登录信息存在,替换用户图标为用户信息的image,并移除用户图标.
        var img_access_token = '<img src="'+img_token+'" style="width: 20px;border-radius: 10px;">';
        $("#user_role a svg").remove();
        $("#user_role_a").prepend($(img_access_token));
        var lout_li = '<li onclick="loginout()" id="loginout"><a href="javascript:void(0);">退出</a></li>';
        //登录信息存在时，用户登录后，添加退出按钮功能。
        $("#person_center").append($(lout_li));
    }else{
        // 否则：移除退出按钮功能.
        $("#loginout").remove();
    }
});



// 初始化搜索结果:ajax渲染搜索结果数据.
$(function () {
    var keyword = window.location.search.substring(1);
    if(keyword.indexOf("keyword=")===-1){
        // 如果地址栏中不存在搜索关键词keyword, 表明此状态为推荐状态.随机搜索10条数据.
        var uid= sessionStorage.getItem("uid");
        $.ajax({
            url: url+"/api/random-recommend/?uid="+uid,
            type: "GET",
            async: false,
            contentType: false,
            dataType: 'json',
            processData: false,
            success: function (json) {
                if(json.status ===200){
                    $("#page_split li").remove();
                    var data = (json.response[0]);
                    $('#content-card .col-md12').remove();
                    if (data.hits.total === 0){
                        //查询的数据数量为0
                    }else{
                        // 查询的数量不为0
                        var hits = data.hits;
                        $.each(hits.hits, function(index, value) {
                            card(value);        // 遍历循环数据后渲染前端页面.
                        });
                        var $p = '<p class="flush_message" onclick="flush_message()" style="text-align: center;width: 100%;height: 25px;\n' +
                            'cursor: pointer;margin: 0 0 -21px;line-height: 25px">刷新</p>';
                        $('#content-card').append($($p));       // 添加刷新按钮.
                    }
                }else{
                    console.log("查询失败.")
                }

            }, error: function (e) {
                alert("ERROR")
            }
        })
    }else{
        // 否则：地址栏中存在搜索关键词keyword，按照搜索关键词搜索数据.
        search(keyword);
        $("#keyword").val(decodeURI(keyword.split('&')[0].toString().split('=')[1])); //搜索关键词后，input输入框填充关键词.
    }
});


// 搜索封装函数
function search(paramter) {
    history.pushState(null, '', '?'+paramter);
    var uid = window.sessionStorage.getItem("uid");
    $.ajax({
        url: url+"/api/search/?"+paramter+'&uid='+uid,
        type: "GET",
        async: false,
        contentType: false,
        dataType: 'json',
        processData: false,
        success: function (json) {
            if(json.status ===200){
                $("#page_split li").remove();
                $(".alert-info").remove();
                var data = (json.response[0]);
                var page = json.response[1];
                $('.flush_message').remove();
                $('#content-card .col-md12').remove();
                if (data.hits.total === 0){
                    //查询的数据数量为0
                }else{
                    // 查询的数量不为0
                    var hits = data.hits;
                     var time_p = ' <div class="alert alert-info" role="alert" style="text-align: right;">\n' +
        '                <p>本次查询已找到<strong style="color: red">'+page.data_count+'</strong>条数据,耗时&nbsp;<strong style="color: red">'+page.time_consume+'</strong>ms</p>\n' +
        '            </div>'
                    $('#containers-row').prepend($(time_p)) ;
                    pagination(page);
                    $.each(hits.hits, function(index, value) {
                        card(value);
                    });
                }
            }else{

            }
        }, error: function (e) {
            alert("search-ERROR")
        }
    });
    $("html").animate({scrollTop:0},10);
     killRepeat(decodeURI(paramter.split('&')[0].toString().split('=')[1]));
    localStorage.search = searchArr;
}



// html 卡片,列表数据的html标签封装函数
function card(data) {
    var div = '<div class="col-md12">\n' +
        '                                <div class="panel panel-default">\n' +
        '                                    <div class="panel-body">\n' +
        '                                        <a href="'+data._source.article_link+'" target="_blank"><h2>'+highlight_title_data(data)+'</h2></a>\n' +
        '                                        <div class="content" style="word-break: break-all;margin-bottom: 12px;">\n' +
        '                                            <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'+highlight_desc_data(data)+'' +
        // '                                            <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'+data._source.article_desc+'' +
        '                                        </div>\n' +
        '                                        <div class="panel-footer">\n' +
        '                                            <i class="glyphicon glyphicon-user"></i>\n' +
        '                                            <span class="article_user">'+data._source.nick_name+'</span>\n' +
        '                                            <i class="glyphicon glyphicon-eye-open"></i>\n' +
        '                                            <span class="article_views">'+data._source.views+'</span>\n' +
        '                                            <i class="glyphicon glyphicon-comment"></i>\n' +
        '                                            <span class="article_comments">'+data._source.comments+'</span>\n' +
        '                                            <i class="glyphicon glyphicon-thumbs-up"></i>\n' +
        '                                            <span class="article_digg">'+data._source.digg+'</span>\n' +
        '                                            <i class="glyphicon glyphicon-calendar"></i>\n' +
        '                                            <span class="article_time">时间</span>\n' +
        '                                            <i class="glyphicon glyphicon-signal"></i>\n' +
        '                                            <span class="article_score">'+data._score+'</span>\n' +'' +
        '                                             <i class="glyphicon glyphicon-share-alt"></i>\n'+
        '                                            <span class="article_from">'+data._source.source+'</span>\n' +'' +
        '                                        </div>\n' +
        '                                    </div>\n' +
        '                                </div>\n' +
        '                            </div>';


    $("#content-card").append($(div));
}


// 文章标题的高亮显示封装函数
function highlight_title_data(data){
    var keyword = window.location.search.substring(1);
    if(keyword.indexOf("keyword=")===-1){
        return data._source.article_title;
    }else{
        if(data.highlight.article_title){
            return data.highlight.article_title;
        }else{
            return data._source.article_title;
        }
    }

}

// 文章描述的高亮显示封装函数
function highlight_desc_data(data){
    var keyword = window.location.search.substring(1);
    if(keyword.indexOf("keyword=")===-1){
        return data._source.article_desc;
    }else{
         if(data.highlight.article_desc){
            return data.highlight.article_desc;
        }else{
            return data._source.article_desc
        }
    }
}



//分页：  -----> 非当前页点击触发事件
$('.page_split2').off('click').on("click", '.page_num', function () {
    var cur_page = $(this).attr('page');
    var keyword = window.location.search.substring(1).split('&')[0]+'&cur_page='+cur_page;
    search(keyword);
});

//分页：  -----> 上一页点击触发事件
$('.page_split').off('click').on("click", '#prev_page_num', function () {
    var cur_page = parseInt($('#cur_page').attr('page')) - 1;
    var keyword = window.location.search.substring(1).split('&')[0]+'&cur_page='+cur_page;
    search(keyword);
});

//分页：  ----->下一页点击触发事件
$('#page_split').off('click').on("click", '#next_page_num', function () {
    var cur_page = parseInt($('#cur_page').attr('page')) + 1;
    var keyword = window.location.search.substring(1).split('&')[0]+'&cur_page='+cur_page;
    search(keyword);
});



//搜索：  ----->index.html 顶端(top)点击搜索图标搜索
$('#search_button').click(function () {
    var keyword = $("#keyword").val().replace(/^\s+|\s+$/g, "");
    var paramter = 'keyword='+keyword+'&cur_page=1';
    $("#suggestion-list ").css('display','none');
    $("#suggestion-list .suggest-li").remove();
    search(paramter);

});

//搜索：   ----->index.html 顶端(top)回车键搜索
$("#keyword").unbind("keypress").bind("keypress", function(event) {
    $("#suggestion-list ").css('display','none');
    $("#suggestion-list .suggest-li").remove();
    if (event.keyCode === 13) { //keyCode=13为回车键
        var keyword = $("#keyword").val().replace(/^\s+|\s+$/g, "");
        var paramter = 'keyword='+keyword+'&cur_page=1';
        search(paramter);
        killRepeat(decodeURI(paramter.split('&')[0].toString().split('=')[1]));
        localStorage.search = searchArr;
        MapSearchArr(searchArr);
    }
});



//搜索输入框focus时,搜索图标变红.
$('#keyword').focus(function () {
    $("#search_button").css('color','red');
});


//搜索失焦后,图标颜色变白,自动提示去除.
$('#keyword').blur(function () {
    $("#search_button").css('color','white');
    $("#suggestion-list .suggest-li").remove();
    $("#suggestion-list ").css('display','none');
});



//搜索建议列表:当用户搜索输入时,会出现搜索建议列表.
$('#keyword').bind('input propertychange ',function () {
    var searchText = $(this).val();
    $.ajax({
        url: url+"/api/suggest/?keyword="+searchText,
        type: "GET",
        async: false,
        contentType: false,
        dataType: 'json',
        processData: false,
        success: function (json) {
            $("#suggestion-list div").remove();
            if(json.status === 200){
                if(json.response.length !==0){
                    $("#suggestion-list").show();
                    $.each(json.response,function (i,value) {
                        var li = '<div class="suggest-li"><a href="#">'+value+'</a></div>';
                        $("#suggestion-list").append($(li))
                    })
                }else{
                    $("#suggestion-list").hide();
                }
            }
        }
    })
});

$(function () {
    spiderdata()
});

// 获取数据来源：爬取的网站和对应爬取的数量.
function spiderdata() {
    // 获取数据来源：爬取的网站和对应爬取的数量.
    $.ajax({
        url: url+"/api/spider-data/",
        type: "GET",
        async: false,
        contentType: false,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            if(json.status === 200){
                if(json.response.length !== 0){
                    $.each(json.response,function (i,val) {
                        var div = '<div class="ssssss"><p><strong class="strong-name">'+val.key+'</strong>:<span class="data-counter" style="color: red;">'+val.doc_count+'</span>条数据</p></div>'
                        $('#data-content').append($(div));
                    })
                }else{
                    console.log("此时数据为空.");
                }
            }else{
                console.log("spider-data数据请求失败.")
            }
        }
    })
}






if(localStorage.search){
    searchArr = localStorage.search.split(',')
}else{
    searchArr = []
}
MapSearchArr(searchArr);



function MapSearchArr(searchArr) {
    var tempHtml = "";
    var arrlen = 0;
    if(searchArr.length>5){
        arrlen = 5

    }else {
        arrlen = searchArr.length;
    }
    $("#my-panel-body p").remove();
    for(var i=0;i<arrlen;i++){
        tempHtml += '<p><a href="'+url+'/result/?keyword='+searchArr[i]+'&cur_page=1'+'">'+searchArr[i]+'</a></p>';
    }
    $('#my-panel-body').append(tempHtml)
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



// $(function(){
// 		var navList = [
// 		  {
// 		    "p" : "热门分类",
// 		    "c" : ["Python","Java","C语言","GoLand","Javascript","PHP"],
//             "icon":"glyphicon glyphicon-list-alt"
// 		  },
// 		  {
// 		    "p" : "博主推荐",
// 		    "c" : ["坚固66","规格严格-功夫到家","梦想天空（山边小溪）","dudu","mengfanrong","每天都要进步一点点"],
//             "icon":"glyphicon glyphicon-fire"
// 		  },
// 		  {
// 		    "p" : "原创社区",
// 		    "c" : ["利通区","红寺堡区","盐池县","同心县","青铜峡市"],
//             "icon":"glyphicon glyphicon-sunglasses"
// 		  },
// 		  {
// 		    "p" : "数据来源",
// 		    "c" : ["CSDN","博客园","开源中国","知乎","彭阳县"],
//             "icon":"glyphicon glyphicon-magnet"
// 		  },
//             {
// 		    "p" : "爬虫后台",
// 		    "c" : [],
//             "icon":"glyphicon glyphicon-magnet"
// 		  }
// 		]
// 		var navData = '';
// 		for(let i=0;i<navList.length;i++){
// 			navData+= "<li class='nav-item'><a href='javascript:;'><i class='"+navList[i].icon+"'></i><span>"+navList[i].p+"</span></a>"
// 			// for(let w=0;w<navList[i].c.length;w++){
// 			// 	navData+="<li><a href='javascript:;'><span>"+navList[i].c[w]+"</span></a></li>"
// 			// }
// 			navData+="</li>"
// 		}
// 		// console.log(navData)
// 		$('#apt').html(navData)
// 	})


// 推荐状态下刷新按钮触发事件.
function flush_message() {
     layui.use('layer', function () {
        var layer = layui.layer;
        var rage = layer.load(3);
        var uid = sessionStorage.getItem("uid");
        $.ajax({
            url: url+"/api/random-recommend/?uid="+uid,
            type: "GET",
            async: false,
            contentType: false,
            dataType: 'json',
            processData: false,   // jQuery不要去处理发送的数据
            success: function (json) {
                if(json.status ===200){
                var data = json.response[0];
                    if (data.hits.total === 0){
                        //查询的数据数量为0
                    }else{
                        // 查询的数量不为0
                        var hits = data.hits;
                        $('.flush_message').remove();
                        $.each(hits.hits, function(index, value) {
                            card(value);
                        });
                        var $p = '<p class="flush_message" onclick="flush_message()" style="text-align: center;width: 100%;height: 25px;\n' +
                            '    cursor: pointer;\n' +
                            '    margin: 0 0 -21px;line-height: 25px">刷新</p>';
                        $('#content-card').append($($p));
                        layer.close(rage)
                    }
                }else{

                }
            }, error: function (e) {
                alert("ERROR")
            }
        })
    })
}



// 退出按钮触发事件.
function loginout() {
    sessionStorage.clear();
    $('#user_role_a img').remove();
    var svg = '<svg class="bi bi-person-fill" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style="    width: 1.5em;\n' + 'height: 1.5em;">\n' + '<path fill-rule="evenodd" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" clip-rule="evenodd"/>\n' + '                            </svg>'
    $("#user_role_a").prepend($(svg));
    layui.use('layer', function () {
        var layer = layui.layer;
        var index = layer.msg("用户退出成功!", {
            time: 2000,
        });
        layer.style(index, {
                "margin":'250px auto',
                width: '400px',
                height:'50px'
                });
    });
    $("#loginout").remove();
}


$(function () {
    $.ajax({
        url: url+"/api/bloger-recommend/",
        type: "GET",
        async: false,
        contentType: false,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            if(json.status === 200){
                var ul = '<ul class="bloger-recommend" style="position: absolute;left: -220px;width: 220px;">';
                $.each(json.response,function (i,val) {
                    var lis = ' <li><a href="'+val.url+'" target="_blank"><span>'+val.key+'('+val.doc_count+')'+'</span></a></li>';
                    ul += lis;
                });
                $('#bloger_list').append($(ul+'</ul>'))
            }else{
                $('#bloger_list ul').remove();
            }
        },error:function () {
            alert("error")
        }
    });
});



