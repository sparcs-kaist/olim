var Data = {};

var Filesys = {
    initialize:function(){
        this.data = [];

        this.registerHandlers();
        this.getListFilesys();
    },
    registerHandlers:function(){
    },
    getListFilesys:function(){
        $.ajax({
            type: 'GET',
            url: '/filesys/getlist/',
            data : {'this_dir': Data.this_dir},
            dataType: 'json',
            success: $.proxy(function(resObj){
                this.addListItems(resObj);
            }, this),
            error: $.proxy(function(xhr){

            }, this)
        });
    },
    addListItems:function(listData){
        this.data = listData;

        if(this.data.dir_list.length == 0 && this.data.file_list.length == 0){
            var tag = 
                '<tr class="list-body-nothing">' +
                    '<td class="body-nothing">There is no file in this dir.</td>' +
                '</tr>';

            $('tbody tr:last').after(tag);
        }else{
            var dir_list_length = this.data.dir_list.length;
            var file_list_length = this.data.file_list.length;

            // Adding dir data.
            for(var i=0;i<dir_list_length;i++){
                var dir = this.data.dir_list[i];
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
                var file = this.data.file_list[i];
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
    },
}
