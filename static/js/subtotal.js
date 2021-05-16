let quantity = document.getElementsByClassName('quantity')
let price = document.getElementsByClassName('price')
let subtotal = document.getElementsByClassName('subtotal')
let total = document.getElementById('total')
let tot
function subTotal() {
    tot = 0
    for (let i = 0; i < price.length; i++) {
        subtotal[i].innerText = (price[i].value) * (quantity[i].value) + " MAD"
        tot += (price[i].value) * (quantity[i].value)
    }
    total.innerText = tot + " MAD";
}
subTotal()