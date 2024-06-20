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


$(document).ready(function() {
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
});