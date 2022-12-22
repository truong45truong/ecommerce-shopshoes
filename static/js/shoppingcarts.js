$(document).ready(()=>{
    var number = $('.quantity-product').val()
    console.log(number)
    $('.select-transport').change(function() {
        $('.price-sport').empty();
        $('.price-sport').append('<p>'+this.value +'</p>');_
    })
    const onChangeSetSession = () => {
        sessionStorage.setItem("quantity", "Smith");
    }
    $('.check-select-product').change(function() {
        if (sessionStorage.getItem('productPay')){
            var listProductPay = sessionStorage.getItem('productPay').split(',')
            console.log('quantity',$('.quantity-'+this.value))
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
        console.log(this.checked,this.value)
    })
})