// 要素をクリックした時、隠れているメニュー要素をフェードイン、アウトのアニメーションで表示非表示にする
function fadeInOut(clickDiv, hiddenElement) {
    $(document).ready(function(){
        $(clickDiv).click(function(e){
            $(hiddenElement).fadeToggle();
        });
        $(document).click(function(e){
            if (!$(e.target).closest(clickDiv).length && !$(e.target).closest(hiddenElement).length) {
                // clickDivもしくはhiddenElement以外の要素がクリックされた時、hiddenElementをフェードアウトさせる
                $(hiddenElement).fadeOut();
            }
        });
    });
}

// 要素をクリックした時、隠れているメニュー要素をフェードイン、アウトのアニメーションで表示非表示にする
function fadeInOut(clickDiv, hiddenElement) {
    $(document).ready(function(){
        $(clickDiv).click(function(e){
            $(hiddenElement).fadeToggle();
        });
        $(document).click(function(e){
            if (!$(e.target).closest(clickDiv).length && !$(e.target).closest(hiddenElement).length) {
                $(hiddenElement).fadeOut();
            }
        });
    });
}

