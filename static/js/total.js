let subtotal = document.getElementsByClassName('subtotal')
let total = document.getElementById('total')
let tot = 0
function Total() {
    tot = 0
    for (let i = 0; i < subtotal.length; i++) {
        tot += Number(subtotal[i].innerText)
    }
    total.innerText = tot + " MAD";
}
Total()
