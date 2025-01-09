const productCategories = {
    "shirts": "Футболка",
    "hoodies": "Толстовка",
    "caps": "Кепка"
}

document.addEventListener('DOMContentLoaded', async () => {
    let products = await fetch("products.json");
    products = await products.json();
    
    populateCards(products['products'], productCategories);
});

function populateCards(products) {
    products.forEach((product) => {
        const container = document.getElementById(product.category);
        const card = createCard(product);
        container.appendChild(card);
    });    
}

function createCard(product) {

    const card = document.createElement("div");
    card.classList.add("card");
    
    const img = document.createElement("img");
    img.src = product.image;
    const handleCardClick = () => goToProduct(product);
    img.addEventListener(`click`, handleCardClick);
    card.appendChild(img);
    
    const price = document.createElement("p");
    price.textContent = `${product.price} ₽`;
    card.appendChild(price);

    const productType = document.createElement("p");
    productType.textContent = productCategories[product.category];
    card.appendChild(productType);

    const title = document.createElement("h2");
    title.textContent = product.name;
    card.appendChild(title);

    const button = document.createElement("button");
    const handleProductClick = () => addToCart(product);
    button.addEventListener(`click`, handleProductClick);
    button.textContent = "Добавить";
    card.appendChild(button);
    
    return card;
}

function addToCart(product) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    if (!cart.includes(product.id)) {
        cart.push(product.id);
        localStorage.setItem('cart', JSON.stringify(cart));
        alert(`Продукт "${product.name}" добавлен в корзину.`);
    }
}
function getCartItems() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function goToProduct(product) {
    location.assign(`product.html?id=${product.id}`);
}