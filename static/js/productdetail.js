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
    
    $(`.addToCartBtn`).click(function (e) {
        e.preventDefault()

        var product_slug = $(this).closest(`.product_data`).find(`.prod_slug`).val()
        var product_size = $(this).closest(`.product_data`).find(`.prod_size`).val()
        var product_qty = $(this).closest(`.product_data`).find(`.qty-item`).val()
        var token = $(`input[name-csrfmiddlewaretoken]`).val()

        $.ajax({
            method: "POST",
            url: "/order/addtocart",
            data: {
                'product_slug': product_slug,
                'product_size': product_size,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            dataType: "dataType",
            success: function (response) {

            }
        })
    })

    $(".prod_size").click(function() { 
        // assumes element with id='button'
        $(".quantityAvail").toggle();
    });
})