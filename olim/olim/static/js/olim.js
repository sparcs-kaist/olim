var Data = {};

var Filesys = {};

Filesys.initialize = function(){
    this.registerHandlers();
    this.getListFilesys();
};

Filesys.registerHandlers = function(){
};

Filesys.getListFilesys = function(){
    $.ajax({
        type: 'GET',
        url: '/filesys/getlist/',
        data : {'this_dir': Data.this_dir},
        dataType: 'json',
        success: function(resObj){
            Filesys.addListItems(resObj);
        },
        error: function(xhr){
        }
    });
};

Filesys.addListItems = function(listData){
    Filesys.data = listData;
    Data.filesys = listData;

    if(Filesys.data.dir_list.length == 0 && Filesys.data.file_list.length == 0){
        var tag = 
            '<tr class="list-body-nothing">' +
                '<td class="body-nothing">There is no file in this dir.</td>' +
            '</tr>';

        $('tbody tr:last').after(tag);
    }else{
        var dir_list_length = Filesys.data.dir_list.length;
        var file_list_length = Filesys.data.file_list.length;

        // Adding dir data.
        for(var i=0;i<dir_list_length;i++){
            var dir = Filesys.data.dir_list[i];
            var secured = '';
            console.log(dir.is_secured);
            if(dir.is_secured){
                secured = 'secured';
            }
            var tag =
                '<tr class="list-body-dir" onclick="' + "location.replace('" + dir.url + "')" + '">' +
                    '<td class="body-name ' + secured + '">' + dir.name + '</td>' +
                    '<td class="body-format">' + dir.format + '</td>' +
                    '<td class="body-uploader">' + dir.uploader + '</td>' +
                    '<td class="body-date">' + dir.date + '</td>' +
                '</tr>';

            if(i == 0 && Data.this_dir == "root"){
                $('tbody').html(tag);
            }else{
                $('tbody tr:last').after(tag);
            }
        }
        // Adding file data.
        for(var i=0;i<file_list_length;i++){
            var file = Filesys.data.file_list[i];
            var secured = '';
            if(file.is_secured){
                secured = 'secured';
            }
            var tag = 
                '<tr class="list-body-file" onclick="' + "location.replace('" + file.url + "')" + '">' +
                    '<td class="body-name ' + secured + '">' + file.name + '</td>' +
                    '<td class="body-format">' + file.format + '</td>' +
                    '<td class="body-uploader">' + file.uploader + '</td>' +
                    '<td class="body-date">' + file.date + '</td>' +
                '</tr>';

            if(i == 0 && dir_list_length == 0){
                $('tbody').html(tag);
            }else{
                $('tbody tr:last').after(tag);
            }
        }
    }
};

var Popup = {};

Popup.initialize = function(){
    if(Data.is_auth == "True"){
        $("button.login").hide();
    }else{
        $("div.auth-user").hide();
    }

    Popup.popup_bg = $("#wrapper-popup");

    Popup.btn_login = $("button.login")[0];
    Popup.sec_login = $("#popup-login");

    Popup.registerHandlers();
};

Popup.registerHandlers = function(){
    $(Popup.btn_login).bind('click', Popup.popupLogin);
};

Popup.popupClose = function(elem){
    $(Popup.popup_bg).fadeTo(100, 0, function(){
        $(this).hide();
    });
    $(elem).fadeTo(50, 0, function(){
        $(this).hide();
    });
};

Popup.popupLogin = function(){
    $(Popup.popup_bg).fadeTo(50, 1);
    $(Popup.sec_login).fadeTo(200, 1);

    var username_input = $("input#username");
    var password_input = $("input#password");
    var submit_button = $("button#submit");
    var close_btn = $(Popup.sec_login).find("button.popup-close");

    $(username_input).focus();

    $(close_btn).click(function(){
        Popup.popupClose($(Popup.sec_login));
    });

    var login_form = $(Popup.sec_login).find("form");

    $(login_form).submit(function(){
        $(username_input).attr('disabled', 'disabled');
        $(password_input).attr('disabled', 'disabled');
        $(submit_button).attr('disabled', 'disabled').addClass('disabled');

        var username = $(username_input).val();
        var password = $(password_input).val();
        var login_data = {
            'username': username,
            'password': password,
        };

        var request = $.ajax({
            type: 'POST',
            url: '/login/',
            data: login_data,
        });

        // Login Successed
        request.done(function(msg){
            $(Popup.btn_login).hide();
            $("div.auth-user").show();
            $("div.auth-user").find("button.user-menu").html(msg);
            Popup.popupClose($(Popup.sec_login));
        });
        // Login Failed
        request.fail(function(err){
            $(username_input).removeAttr('disabled');
            $(password_input).removeAttr('disabled');
            $(submit_button).removeAttr('disabled').removeClass('disabled');

            var i = 0
            var anime = function(){
                i++;
                $(Popup.sec_login).animate({
                    "background-color": "#fff4e2"
                }, 200, function(){
                    $(this).animate({
                        "background-color": "#fff"
                        }, 200, function(){
                            if(i < 2){
                                anime();
                            }else{
                                $(username_input).focus();
                            }
                        });
                });
            };
            anime();
        });
    });
};

Popup.userMenu = function(){

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
        },
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
