const productCategories = {
    "shirts": "Футболка",
    "hoodies": "Толстовка",
    "caps": "Кепка"
}


document.addEventListener('DOMContentLoaded', async () => {
    const product = await getProduct();
    displayProduct(product);
});

async function getProduct() {
    let products = await fetch("products.json");
    products = await products.json();
    products = products['products'];
    const urlParams = new URLSearchParams(window.location.search);
    const productId = Number (urlParams.get('id'));
    console.log(products);
    const product = products.find((p) => {return p.id === productId });
    console.log(product);
    return product;
};

function displayProduct(product) {
    if (product !== null) {
        const title = document.getElementById('product-title');
        const category = document.getElementById('product-category');
        const image = document.getElementById('product-image');
        const price = document.getElementById('product-price');
        const button = document.getElementById('product-button');
        const description = document.getElementById('product-description');
        const characteristics = document.getElementById('product-characteristics');

        document.title = `MineShop - ${product.name}`;
        title.textContent = product.name;
        category.textContent = productCategories[product.category];
        image.src = product.image;
        price.textContent = `${product.price} ₽`;
        const handleProductClick = () => addToCart(product);
        button.addEventListener('click', handleProductClick);
        description.textContent = product.description;

        Object.entries(product.characteristics).forEach(([key, value]) => {
            const characteristicDiv = document.createElement('div');
            
            const keyParagraph = document.createElement('b');
            keyParagraph.textContent = key + ':';
            characteristicDiv.appendChild(keyParagraph);

            const valueParagraph = document.createElement('p');
            valueParagraph.textContent = value;
            characteristicDiv.appendChild(valueParagraph);

            characteristics.appendChild(characteristicDiv);
        });
        
    }else {
        const title = document.getElementById('product-title');
        const item = document.getElementById('product-item');
        const description = document.getElementById('product-description');

        document.title = 'Товар не найден';
        title.textContent = 'Товар не найден';
        item.style.display = 'none';
        description.style.display = 'none';
    }
}

function addToCart() {

}

