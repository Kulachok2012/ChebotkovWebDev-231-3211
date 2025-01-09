const productCategories = {
    "shirts": "Футболка",
    "hoodies": "Толстовка",
    "caps": "Кепка"
}

document.addEventListener('DOMContentLoaded', async () => {
    let products = await fetch("products.json");
    products = await products.json();
    
    fillCart(products['products'], getCartItems());
});

function getCartItems() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}
async function fillCart(products, cart) {
    const table = document.querySelector('#cart-table tbody');
    const totalPriceElement = document.getElementById('total-price');
    let totalPrice = 0;

    for (let i = 1; i <= cart.length; i++) {
        const product = products.find((p) => {return p.id === cart[i-1]});
        totalPrice += product.price;
        await pushToTable(table, i, product);
    }
    totalPriceElement.textContent = `Итого: ${totalPrice} ₽`;
}

async function pushToTable(table, index, product) {
    let newRow = table.insertRow();
    let numCell = newRow.insertCell();
    let numText = document.createTextNode(index);
    numCell.appendChild(numText);

    let titleCell =  newRow.insertCell();
    let titleText = document.createTextNode(product.name);
    titleCell.appendChild(titleText);

    let typeCell = newRow.insertCell();
    let typeText = document.createTextNode(productCategories[product.category]);
    typeCell.appendChild(typeText);

    let priceCell = newRow.insertCell();
    let priceText = document.createTextNode(`${product.price} ₽`);
    priceCell.appendChild(priceText);

    let actionsCell = newRow.insertCell();
    const actionsDiv = document.createElement('div');
    actionsDiv.classList.add('actions');

    const deleteButton = document.createElement('button');
    const handleDeleteClick = () => removeCartElement(product.id);
    deleteButton.addEventListener('click', handleDeleteClick);
    const deleteImg = document.createElement('img');
    deleteImg.src = 'images/delete.svg';
    deleteButton.appendChild(deleteImg);
    actionsDiv.appendChild(deleteButton);
    actionsCell.appendChild(actionsDiv);
}

async function removeCartElement(id) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    if (cart.indexOf(id) !== -1) {
        cart.splice(cart.indexOf(id), 1);
        localStorage.setItem('cart', JSON.stringify(cart));
        location.reload();
    } else {
        console.log(`Товар с ID ${id} не найден в корзине.`);
    }
}