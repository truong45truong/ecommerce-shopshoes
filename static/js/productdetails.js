$(document).ready(function () {
    $(`.increment-btn`).click(function (e) {
        e.preventDefault()
        var incre_value = $(this).closest(`.product_data`).find(`.qty-item`).val()
        var value = parseInt(incre_value,10)
        value = isNaN(value) ? 0 : value
        if(value < 10)
        {
            value++
            $(this).closest(`.product_data`).find(`.qty-item`).val(value)
        }
    })
    $(`.decrement-btn`).click(function (e) {
        e.preventDefault()
        var decre_value = $(this).closest(`.product_data`).find(`.qty-item`).val()
        var value = parseInt(decre_value,10)
        value = isNaN(value) ? 0 : value
        if(value > 1)
        {
            value--
            $(this).closest(`.product_data`).find(`.qty-item`).val(value)
        }
    })
    
    $('#addToCartBtn').click(function (e) {
        e.preventDefault()
        console.log("runnning add to cart")
        var product_slug = $(this).closest(`.product_data`).find(`.prod_slug`).val()
        var product_size = false
        var product_qty = $(this).closest(`.product_data`).find(`.qty-item`).val()
        var headers = {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() };

        for (i of document.getElementsByClassName("prod_size")){
            if(i.checked == true){
                product_size = i.value
            }
        }
        $.ajax({
            method: "POST",
            url: "/order/addtocart",
            contentType: "json",
            headers: headers,
            data:JSON.stringify({
                slug : product_slug,
                sizes: product_size,
                quantity : product_qty,
            }),
            success: function (response) {
                alert("đã thêm sản phẩm vào giỏ hàng")
            }
        })
    })

    $(".prod_size").click(function() { 
        // assumes element with id='button'
        $(".quantityAvail").show();
    });
})