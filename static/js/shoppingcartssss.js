$(document).ready(()=>{
    sessionStorage.setItem('productPay',[])
    var number = $('.quantity-product').val()
    console.log(number)
    const uploadPayment = () =>{
        var listProductPay = sessionStorage.getItem('productPay').split(',')
        hrefPay = document.getElementById('pay-product').href
        hrefPay += '?productPay=';
        for (oj of listProductPay){
            hrefPay = hrefPay + oj +"_"
        }
        hrefPay += '&transport='
        hrefPay += document.getElementById('select-transport-pay').value

        console.log(hrefPay,document.getElementById('select-transport-pay'))
        if(listProductPay.length == 0){
            alert("bạn chưa chọn đầy đủ thông tin")
        } else {
            hrefPay = document.getElementById('pay-product').href
            hrefPay += '?productPay=';
            for (oj of listProductPay){
                hrefPay = hrefPay + oj +"_"
            }
            hrefPay += '&transport='
            hrefPay += document.getElementById('select-transport-pay').value

            console.log(hrefPay,document.getElementById('select-transport-pay'))
            document.getElementById('pay-product').href=hrefPay
        }
    }
    $('.select-transport').change(function() {
        $('.price-sport').empty();
        $('.price-sport').append(this.title);_
        uploadPayment()
    })
    const onChangeSetSession = () => {
        sessionStorage.setItem("quantity", "Smith");
    }
    const uploadTotalSelectProduct = () =>{
        $('.total-product-select').empty()
        sum = 0 
        var listProductPay = sessionStorage.getItem('productPay').split(',')
    
        for( i of listProductPay){
            sum += parseInt(i.split(":")[1])
        }
        $('.total-product-select').append(sum)
    }
    $('.check-select-product').change(function() {
        if (sessionStorage.getItem('productPay')){
            var listProductPay = sessionStorage.getItem('productPay').split(',')
            if(this.checked == true){
                listProductPay.push(this.value+":"+$('.quantity-'+this.value).attr('value'))
            }
            if(this.checked == false){
                listProductPay= listProductPay.filter(item =>  item.split(":")[0] != this.value)
            }
            sessionStorage.setItem('productPay',listProductPay)
        }else {
            if(this.checked == true){
                sessionStorage.setItem('productPay',[this.value+":"+$('.quantity-'+this.value).attr('value')])
            }
        }
        uploadTotalSelectProduct()
    })

    $(".remove-to-cart").click(function(){
        data = $(this).attr("value").split('_')
        var headers = {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() };
        var data_response =[]
        console.log(data)
        $.ajax({
            type:'POST',
            url:"/order/removetocart",
            contentType: "json",
            data:JSON.stringify({
                slug:data[0],
                sizes:data[1],
                quantity:data[2]
            })
            ,
            
            success:function(response){
                data_response = response
                $('.data-product').empty()
                for (item of JSON.parse(data_response)){
                    str = "<div class='list-item-cart py-3'>"
                        +   "<div id='item-cart' class='row mb-4 d-flex justify-content-between align-items-center'>"
                        +       "<div class='col-md-2 col-lg-2 col-xl-2 d-flex'>"
                        +           "<input class='me-2 check-select-product' id='checked-"+item.slug+"-"+item.size+"' type='checkbox' value='"+item.slug+"-"+item.size+"'>"
                        +           "<img src='/media/photos/products/"+ item.photo+"' class='img-fluid rounded-3' alt='Cotton T-shirt'>"
                        +       "</div>"
                        +       "<div class='col-md-3 col-lg-3 col-xl-3'>"
                        +              "<h6 class='text-muted'>Size : <p class='d-inline'>"+ item.size +"</p> </h6>"
                        +               "<div class='gender-item'>"
                    if (item.sex == 1 ) str = str + "<h6 class='text-muted'>Men</h6>"
                    if (item.sex == 2 ) str = str + "<h6 class='text-muted'>Women</h6>"
                    if (item.sex == 0 ) str = str + "<h6 class='text-muted'>All</h6>"
                    str = str +"</div>"
                        +               "<h6 class='text-black mb-0'>"+item.name+"</h6>"
                        +       "</div>"
                        +       "<div class='col-md-3 col-lg-3 col-xl-2 d-flex'>"
                        +           "<button class='btn btn-link px-2'"
                        +               'onclick="updateQuantityUp('+"'quantity-"+item.slug+"-"+item.size+"','"+ item.slug +"-"+item.size+"')" +'"' + ">"
                        +               "<i class='fas fa-minus'></i>"
                        +           "</button>"
                        +           "<input class='quantity-product form-control form-control-sm quantity-"+item.slug+"-"+item.size+"' id='form1' min='1' max='"+item.quantityMax+"' name='quantity' value='"+item.quantity+"' type='number'/>"
                        +           "<button class='btn btn-link px-2'"
                        +               'onclick="updateQuantityDown('+"'quantity-"+item.slug+"-"+item.size+"','"+ item.slug +"-"+item.size+"')" +'"' + ">"
                        +               "<i class='fas fa-plus'></i>"
                        +               "</button>"
                        +       "</div>"
                        +       "<div class='col-md-3 col-lg-2 col-xl-2 offset-lg-1'>"
                        +           "<h6 class='mb-0'>"+item.price_total+"</h6>"
                        +       "</div>"
                        +       "<div class='col-md-1 col-lg-1 col-xl-1 text-end'>"
                        +           "<button  class='remove-to-cart text-muted' value='"+item.slug+"_"+item.size+"_"+item.quantity+"' ><i class='fas fa-times'></i></button>"
                        +       "</div>"
                        + "</div>"
                        + "<hr class='my-4 w-100'>"
                        + "</div>"
                        + "<script src='/static/js/shoppingcartssss.js'></script>"
                    $('.data-product').append(str)
                }
            }
        })
    });
})