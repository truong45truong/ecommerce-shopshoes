
const uploadTotalSelectProduct = () =>{
    $('.total-product-select').empty()
    sum = 0 
    var listProductPay = sessionStorage.getItem('productPay').split(',')

    for( i of listProductPay){
        sum += parseInt(i.split(":")[1])
    }
    $('.total-product-select').append(sum)
}

const uploadSessionSelectProductPay = (slug,index) => {
    var listProductPay = sessionStorage.getItem('productPay').split(',')

    listProductPay = listProductPay.filter(item =>  item.split(":")[0] != slug)
    listProductPay.push(slug+":"+index)
    sessionStorage.setItem('productPay',listProductPay)
}

const updateQuantityDown = (classInput,slug) => {
    if(document.getElementById('checked-'+slug).checked==true){
        var index = parseInt($('.'+classInput).attr('value'))+1
        $('.'+classInput).attr('value',index)

        uploadSessionSelectProductPay(slug,index)
        uploadTotalSelectProduct()
    }
}
const updateQuantityUp = (classInput,slug) => {
    if(document.getElementById('checked-'+slug).checked==true){
        var index = parseInt($('.'+classInput).attr('value'))-1
        if( index > 0){
            $('.'+classInput).attr('value',index)
            uploadSessionSelectProductPay(slug,index)
            uploadTotalSelectProduct()
        }
    }
}