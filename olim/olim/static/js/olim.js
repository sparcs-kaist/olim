var Data = {};

// Filesys class
var Filesys = {};

Filesys.initialize = function(){
    Filesys.getUrlData();
};
Filesys.getUrlData = function(inputData){
    if(typeof(inputData) == 'undefined'){
        inputData = {
            'p_dir_id': Data.p_dir.id,
            'p_dir_url': Data.p_dir.url
        }
    }
    $.ajax({
        type: 'GET',
        url: '/filesys/getdata/',
        data: inputData,
        dataType: 'json',
        success: function(resObj){
            Filesys.addQuickPath(resObj);
            Filesys.addListItems(resObj);
        },
        error: function(xhr){
            console.log(xhr.responseText);
        }
    });
};
Filesys.addQuickPath = function(resData){
    // Add quick path items
    Data.quick_path = resData.quick_path;

    for(var i=0; i<Data.quick_path.length; i++){
        var a_last = $('.quickpath-list li:last');
        var q_tag = Tags.quickpath(Data.quick_path[i]);
        if(a_last.length == 0){
            $('.quickpath-list').html(q_tag);
        }else{
            $(a_last).after(q_tag);
        }
    }

    // Store DOM elements
    Filesys.quickPathDOM = $('.quickpath-list a');

    $(Filesys.quickPathDOM).click(function(){
        Filesys.moveDirectory("", $(this).attr("href"));
        return false;
    });
};
Filesys.addListItems = function(resData){
    Data.p_dir = resData.p_dir;
    Data.pp_dir = resData.pp_dir;
    Data.dir_list = resData.dir_list;
    Data.file_list = resData.file_list;

    // Change directory title
    var t_tag = '<span>' + Data.p_dir.name + '</span> directory';
    $('h2.list-title').html(t_tag);

    // Add link row to parent dir
    if(Data.pp_dir != ""){
        var b_tag = Tags.list_body_back(Data.pp_dir);
        $('tbody').html(b_tag);
    }

    // Add dir and file items
    if(Data.dir_list.length == 0 && Data.file_list.length == 0){
        var n_tag = Tags.list_body_nothing();
        $('tbody tr:last').after(n_tag);
    }else{
        for(var i=0; i<Data.dir_list.length; i++){
            var tr_last = $('tbody tr:last');
            var d_tag = Tags.list_body_dir(Data.dir_list[i]);
            if(tr_last.length == 0){
                $('tbody').html(d_tag);
            }else{
                $(tr_last).after(d_tag);
            }
        }
        for(var i=0; i<Data.file_list.length; i++){
            var tr_last = $('tbody tr:last');
            var f_tag = Tags.list_body_file(Data.file_list[i]);
            if(tr_last.length == 0){
                $('tbody').html(f_tag);
            }else{
                $(tr_last).after(f_tag);
            }
        }
    }

    // Store DOM elements
    Filesys.listItemsDOM = $('tbody tr');

    $(Filesys.listItemsDOM).click(function(){
        var item_id = $(this).attr("id");
        var item_sort = item_id.split('-');

        if(item_sort[0] == 'd'){
            Filesys.moveDirectory(item_sort[1], "");
        }else{
            Filesys.fileDownload(item_sort[1], "");
        }
    });
};
Filesys.moveDirectory = function(dir_id, dir_url){
    data = {
        'p_dir_id': dir_id,
        'p_dir_url': dir_url
    }

    $(Filesys.quickPathDOM).remove();
    $(Filesys.listItemsDOM).remove();
    Filesys.getUrlData(data);
};
Filesys.fileDownload = function(file_id, file_url){
    if(file_url == ""){
        $.each(Data.file_list, function(index, item){
            if(item.id == file_id){
                window.open(item.url);
            }
        });
    }else{
        window.open(file_url);
    }
};

// Popup class

var Popup = {};

Popup.initialize = function(){
    if(Data.is_auth){
        $('.header-auth-user').show();
    }else{
        $('.header-login').show();
    }

    Popup.bg = $('#popup-wrapper');
    Popup.login = {
        btn: $('button.login-button'),
        sec: $('section#popup-login'),
        cls: $('button.login-close'),
        form: $('form.login-form'),
        username: $('input#username'),
        password: $('input#password'),
        submit: $('button#submit')
    };
    Popup.umenu = {
        btn: $('button.user-menu-button'),
        sec: $('section#popup-umenu'),
        logout: $('button.logout-button'),
        profile: $('button.profile-button')
    };

    Popup.registerHandlers();
};
Popup.registerHandlers = function(){
    $(Popup.login.btn).bind('click', function(){Popup.popupLogin(true)});
    $(Popup.login.cls).bind('click', function(){Popup.popupLogin(false)});
    $(Popup.umenu.btn).bind('click', function(){Popup.popupUmenu()});
};
Popup.popupBack = function(st){
    if(st){
        $(Popup.bg).fadeTo(50, 1);
    }else{
        $(Popup.bg).fadeTo(100, 0, function(){
            $(this).hide();
        });
    }
};
Popup.popupLogin = function(st){
    if(st){
        Popup.popupBack(true);
        $(Popup.login.sec).fadeTo(100, 1);
        $(Popup.login.username).focus();

        $(Popup.login.form).submit(function(){
            $(Popup.login.username).attr('disabled', 'disabled');
            $(Popup.login.password).attr('disabled', 'disabled');
            $(Popup.login.submit).attr('disabled', 'disabled').addClass('disabled');

            var username = $(Popup.login.username).val();
            var login_data = {
                'username': $(Popup.login.username).val(),
                'password': $(Popup.login.password).val()
            };
            var request = $.ajax({
                type: 'POST',
                url: '/login/',
                data: login_data
            });
            request.done(function(){
                Popup.popupLogin(false);
                $('.header-login').hide(function(){
                    $('.header-auth-user').show();
                    $('.user-menu-button').html(username);
                });

                $(Popup.login.username).val('').removeAttr('disabled');
                $(Popup.login.password).val('').removeAttr('disabled');
                $(Popup.login.submit).removeAttr('disabled').removeClass('disabled')
                Filesys.moveDirectory(Data.p_dir.id, Data.p_dir.url);
            });
            request.fail(function(){
                $(Popup.login.username).removeAttr('disabled');
                $(Popup.login.password).val('').removeAttr('disabled');
                $(Popup.login.submit).removeAttr('disabled').removeClass('disabled')

                var i = 0
                var anime = function(){
                    i++;
                    $(Popup.login.sec).animate({
                        'background-color': '#fff4e2'
                    }, 200, function(){
                        $(this).animate({
                            'background-color': '#fff'
                        }, 200, function(){
                            if(i < 2){
                                anime();
                            }else{
                                $(Popup.login.username).focus();
                            }
                        });
                    });
                };
                anime();
            });
        });
    }else{
        Popup.popupBack(false);
        $(Popup.login.sec).fadeTo(50, 0, function(){
            $(this).hide();
        });
    }
};
Popup.popupUmenu = function(){
    if($(Popup.umenu.sec).css('display') == "none"){
        $(Popup.bg).addClass('umenu-bg');
        $(Popup.bg).fadeTo(50, 1);
        $(Popup.umenu.sec).fadeTo(100, 1);
        $(Popup.umenu.btn).addClass('clicked');

        $(Popup.umenu.logout).click(function(){
            Popup.popupLogout();
        });
        $(Popup.umenu.profile).click(function(){
            alert("PROFILE MENU");
        });
    }else{
        $(Popup.bg).fadeTo(100, 0, function(){
            $(this).hide().removeClass('umenu-bg');
        });
        $(Popup.umenu.sec).fadeTo(50, 0, function(){
            $(this).hide();
        });
        $(Popup.umenu.btn).removeClass('clicked');
    }
};
Popup.popupLogout = function(){
    $(Popup.umenu.logout).hide();
    $('.logout-loading').fadeTo(50, 1);

    var request = $.ajax({
        type: 'POST',
        url: '/logout/'
    });
    request.done(function(){
        Popup.popupUmenu();
        $('.logout-loading').hide();
        $(Popup.umenu.logout).show();

        $('.header-auth-user').hide();
        $('.header-login').show();
        Filesys.moveDirectory(Data.p_dir.id, Data.p_dir.url);
    });
    request.fail(function(){
        $('.logout-loading').hide();
        $(Popup.umenu.logout).show();
    });
};

// Used tags

Tags = {};

Tags.quickpath = function(obj){
    var tag =
        '<li class="quickpath">' +
            '<a href="' + obj.url + '">' + obj.name + '</a>' +
        '</li>';
    return tag;
};
Tags.list_body_back = function(obj){
    var tag =
        '<tr id="d-' + obj.id + '" class="list-body-back">' +
            '<td class="body-back">' +
                'Back to <span>' + obj.name + '</span> directory' +
            '</td>' +
            '<td class="body-format">-</td>' +
            '<td class="body-uploader">-</td>' +
            '<td class="body-date">-</td>' +
        '</tr>';
    return tag;
};
Tags.list_body_nothing = function(){
    var tag = 
        '<tr class="list-body-nothing">' +
            '<td class="body-nothing">There is no file in this dir.</td>' +
        '</tr>';
    return tag;
};
Tags.list_body_dir = function(obj){
    var secured = "";
    if(obj.is_secured){
        secured = " secured";
    }
    var tag =
        '<tr id="d-' + obj.id + '" class="list-body-dir">' +
            '<td class="body-name' + secured + '">' + obj.name + '</td>' +
            '<td class="body-format">' + obj.format + '</td>' +
            '<td class="body-uploader">' + obj.uploader + '</td>' +
            '<td class="body-date">' + obj.date + '</td>' +
        '</tr>';
    return tag;
};
Tags.list_body_file = function(obj){
    var secured = "";
    if(obj.is_secured){
        secured = " secured";
    }
    var tag =
        '<tr id="f-' + obj.id + '" class="list-body-file">' +
            '<td class="body-name' + secured + '">' + obj.name + '</td>' +
            '<td class="body-format">' + obj.format + '</td>' +
            '<td class="body-uploader">' + obj.uploader + '</td>' +
            '<td class="body-date">' + obj.date + '</td>' +
        '</tr>';
    return tag;
};

var Session = {};

Session.initialize = function(){
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            if(!Session.csrfSafeMethod(settings.type)){
                var csrftoken = Session.getCookie('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
};
Session.getCookie = function(name){
    var cookieValue = null;
    if(document.cookie && document.cookie != ''){
        var cookies = document.cookie.split(';');
        for(var i=0; i<cookies.length; i++){
            var cookie = $.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) == (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
Session.csrfSafeMethod = function(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
