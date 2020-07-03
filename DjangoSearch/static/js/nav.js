$(function(){
    // nav收缩展开
    $('#aat').on('click','.nav-item>a',function(){
        if (!$('.nav').hasClass('nav-mini')) {
            if ($(this).next().css('display') == "none") {
                //展开未展开
                $('.nav-item').children('ul').slideUp(300);
                $(this).next('ul').slideDown(300);
                $(this).parent('li').addClass('nav-show').siblings('li').removeClass('nav-show');
                $(this).children('i').eq(1).attr('class','glyphicon glyphicon-menu-down')
            }else{
                //收缩已展开
                $('.nav-item.nav-show').removeClass('nav-show');
                $(this).children('i').eq(1).attr('class','glyphicon glyphicon-menu-right');
                $(this).next('ul').slideUp(300);
            }
        }
    });
    // 标志点击样式
    $('#aat').on('click','.nav-item>ul>li',function(){
    	$('.nav-item>ul>li').css('background','none')
    	$(this).css('background','yellow')
//  	$(this).siblings().css('background','none')
    })


});


