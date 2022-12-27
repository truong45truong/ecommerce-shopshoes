$('#PayOnReceiptBtn').click(function (e) {
    e.preventDefault()
    slug = this.value
    $.ajax({
        method: "POST",
        url: "/payment/payonreceipt",
        contentType: "json",
        data:JSON.stringify({
            slug : slug,
        }),
        success: function (response) {
            document.write(response)
        }
    })
})
// $(window).bind('beforeunload', function(e){
//     e.preventDefault()
//     slug = document.getElementById("PayOnReceiptBtn").value
//     $.ajax({
//         method: "POST",
//         url: "/payment/removepayment",
//         contentType: "json",
//         data:JSON.stringify({
//             slug : slug,
//         }),
//         success: function (response) {
//             document.write(response)
//         }
//     })
//   });