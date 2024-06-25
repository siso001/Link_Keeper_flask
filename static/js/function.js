document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll('.red, .yellow, .green, .blue, .gray');

    elements.forEach(element => {
        const color = element.className.split(' ').find(c => ['red', 'yellow', 'green', 'blue', 'gray'].includes(c));

        if (!color) return;

        if (element.tagName.toLowerCase() === 'th') {
            element.classList.add(`backgroundcolor-${color}`);
        } else {
            element.classList.add(`backgroundimage-${color}`);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const clickableElement = document.querySelector('.clickable');

    clickableElement.addEventListener('click', function() {
        if (clickableElement.classList.contains('clicked')) {
            clickableElement.classList.remove('clicked');
        } else {
            clickableElement.classList.add('clicked');
        }
    });
});

function fadeInOut(clickDiv, hiddenElement) {
    $(document).ready(function(){
        $(clickDiv).click(function(e){
            $(hiddenElement).fadeToggle();
        });
        $(document).click(function(e){
            if (!$(e.target).closest(clickDiv).length) {
                $(hiddenElement).fadeOut();
            }
        });
    });
}


$(document).ready(function() {
    // 追加ボタンとメニューにfadeInOut関数を適用
    fadeInOut(".toolbar-button", ".create-menu");

    $('.after').click(function() {
        var urlId = $(this).data('url-id');  
        var url = '/userpage/' + folderId + '/' + folderName;
        $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json',
            data: JSON.stringify({ url_id: urlId }), 
            success: function(response) {
                console.log('Server response:', response);
                window.location.reload();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    // フォルダ編集ポップアップを開く
    $(".create-folder-href").click(function(e) {
        e.preventDefault();
        var folderName = $(this).data('folder_name');
        var folderColor = $(this).data('folder_color');
        $("#create-folder-name").val(folderName);
        $("#create-folder-color").val(folderColor);
        $("#create-folder-popup").fadeIn();
    });

    // URL編集ポップアップを開く
    // $(".edit-url").click(function(e) {
    //     e.preventDefault();
    //     var urlId = $(this).data('url-id');
    //     var urlName = $(this).data('url-name');
    //     var urlAddress = $(this).data('url-address');
    //     var folderId = $(this).data('folder-id');
    //     $("#edit-url-id").val(urlId);
    //     $("#edit-url-name").val(urlName);
    //     $("#edit-url-address").val(urlAddress);
    //     $("#edit-url-folder").val(folderId);
    //     $("#edit-url-popup").fadeIn();
    // });

    // ポップアップを閉じる
    $(".close-popup").click(function() {
        $(".popup").fadeOut();
    });

    // ポップアップの外側をクリックしたときに閉じる
    // $(document).click(function(e) {
    //     if (!$(e.target).closest('.popup, .edit-folder, .edit-url').length) {
    //         $(".popup").fadeOut();
    //     }
    // });
});