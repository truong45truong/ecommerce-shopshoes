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
            console.log('item',listProductPay)
            if(this.checked == true){
                listProductPay.push(this.value+":1")
            }
            if(this.checked == false){
                listProductPay= listProductPay.filter(item => item = this.value)
            }
            sessionStorage.setItem('productPay',listProductPay)
        }else {
            if(this.checked == true){
                sessionStorage.setItem('productPay',[this.value])
            }
        }
        console.log(this.checked,this.value)
    })
})