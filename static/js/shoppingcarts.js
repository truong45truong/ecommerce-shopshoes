$(document).ready(()=>{
    sessionStorage.setItem('productPay',[])
    var number = $('.quantity-product').val()
    console.log(number)
    $('.select-transport').change(function() {
        $('.price-sport').empty();
        $('.price-sport').append('<p>'+this.value +'</p>');_
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
})