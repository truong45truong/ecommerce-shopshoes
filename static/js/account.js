$(document).ready(()=>{
    var stateBar=false
    $(".account-bar").slideUp(0)
    $(window).resize(function() {
    });
    $(".account-expand").click(function(){
        if(stateBar==false){
            $(".account-bar").slideDown(500)
        }else{
            $(".account-bar").slideUp(500)
        }
        stateBar=!stateBar
    })
})