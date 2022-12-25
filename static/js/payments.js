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
           alert(response)
        }
    })
})