window.scrollTo(0, 800)
var page= window.location.search.replace("?page=","")
$(".pagination li").eq(page).addClass("active-page")
$(document).ready(()=>{
    var list_shopping_cart =  JSON.parse(localStorage.getItem('list_shoppong_cart')) || [];
    $("#addtocart").click(function(){
        var sizes =[]
        var slug = $(this).val()
        $("#list-size-"+slug+" li .btn-check:checked").each(function(){
            console.log("item")
            var item = {
                'size' : $(this).attr('title'),
                'quantity': $("#quantity-product-"+slug).val()
            }
            sizes.push(item)
        })
    
        var headers = {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() };
        $.ajax({
            type:'POST',
            url:"/order/addtocart",
            contentType: "json",
            headers: headers,
            data:JSON.stringify({
                slug:slug,
                sizes:sizes
            })
            ,
            
            success:function(){
                    }
        })
    });

})