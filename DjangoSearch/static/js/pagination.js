function pagination(pagination_info) {
    if (pagination_info.page_end == 0) {
        $('.page_split2').parent().parent().attr('hidden', true)

        layer.msg('抱歉，没有搜到您想要的结果', {
            icon: 2,
            // offset: ['250px', '490px'],
            time: 1200 //2秒关闭（如果不配置，默认是3秒）
        }, function () {
        });
    } else {
        $('.page_split2').parent().parent().attr('hidden', false);
        var data_count = pagination_info.data_count;
        var last_page = pagination_info.last_page;
        var start_page = pagination_info.page_start;
        var end_page = pagination_info.page_end;
        var cur_page = pagination_info.cur_page;
        document.getElementById('page_split').innerHTML = '';
        let ul = document.getElementById('page_split');
        let li_s = document.createElement('li');
        ul.append(li_s);
        let span1 = document.createElement('span');
        span1.setAttribute('style', 'border: 0');
        span1.setAttribute('id', 'page_split_num');
        span1.innerHTML = '共&nbsp;<strong class="page_sum">' + last_page + '</strong>&nbsp;页,&nbsp;<strong class="date_sum">' + data_count + '</strong>条数据';
        li_s.append(span1);
        let lia = document.createElement('li');
        ul.append(lia);
        let li0 = document.createElement('li');
        ul.appendChild(li0);
        let af = document.createElement('a');
        af.setAttribute('style', 'cursor: pointer;');
        af.setAttribute('class', 'page_num');
        af.setAttribute('page', 1);
        af.innerHTML = "&lt&lt";
        lia.append(af);
        let a0 = document.createElement('a');
        a0.setAttribute('id', 'prev_page_num');
        a0.setAttribute('style', 'cursor: pointer;');
        if (cur_page == 1) {
            a0.setAttribute('style', 'pointer-events: none; ');
        }
        a0.innerHTML = '&lt';
        li0.appendChild(a0);

        var flag = start_page;
        for (var i = start_page; i <= end_page; i++) {
            let li = document.createElement('li');
            ul.appendChild(li);
            let name = 'a' + flag.toString();
            name = document.createElement('a');
            name.setAttribute('style', 'cursor: pointer;');
            name.setAttribute('class', 'page_num');
            name.setAttribute('page', i);
            if (cur_page == i) {
                name.setAttribute('class', 'active page_num');
                name.setAttribute('id', 'cur_page');
            }
            name.innerHTML = flag;
            li.appendChild(name);
            flag = flag + 1;
        }
        let li2 = document.createElement('li');
        ul.appendChild(li2);
        let a2 = document.createElement('a');
        a2.setAttribute('id', 'next_page_num');
        a2.setAttribute('style', 'cursor: pointer; ');
        if (cur_page == end_page) {
            a2.setAttribute('style', 'pointer-events: none;');
        }
        a2.innerHTML = '&gt';
        li2.appendChild(a2);
        let lie = document.createElement('li');
        ul.append(lie);
        let ae = document.createElement('a');
        ae.setAttribute('style', 'cursor: pointer;');
        ae.setAttribute('class', 'page_num');
        ae.setAttribute('page', last_page);
        ae.innerHTML = "&gt&gt";
        lie.append(ae);
    }
}
