$(document).ready(()=>{
    var stateBar=false
    $(window).resize(function() {
        if($(window).width() > 768)
            $(".menu").fadeIn(0)
    });
    $("#bar-menu").click(function(){
        width=$(".menu").width()
        $(".menu").fadeIn(0)
        $(".menu").animate({right: 0+'px'})
        stateBar= !stateBar
    })
    $(".bar-exit").click(function(){
        width=$(".menu").width()
        $(".menu").animate({right: -1.2*width+'px'})
        $(".menu").fadeOut(0)
        stateBar= !stateBar
    })
})