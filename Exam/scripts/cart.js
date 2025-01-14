document.addEventListener('DOMContentLoaded', async () => {
    try {
        
        document.getElementById('order-form').addEventListener('submit', submitOrder);
        // Получаем данные о товарах из API
        const response = await fetch("https://edu.std-900.ist.mospolytech.ru/exam-2024-1/api/goods?api_key=e8edbd36-da5f-4862-bda5-06eeb0c60a19");
        if (!response.ok) throw new Error('Ошибка получения данных');
        const products = await response.json();

        // Получаем товары из корзины
        const cartItems = getCartItems();

        // Фильтруем только те товары, которые есть в корзине
        const cartProducts = products.filter(product =>
            cartItems.includes(product.id)
        );

        // Заполняем корзину отфильтрованными товарами
        fillCart(cartProducts);
    } catch (error) {
        console.error('Ошибка:', error);
    }
});

function getCartItems() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

async function fillCart(cartProducts) {
    const container = document.getElementById("productsContainer");
    container.innerHTML = ''; // Очищаем контейнер перед заполнением

    let totalPrice = 0;

    // Создаем карточки для товаров в корзине
    cartProducts.forEach((product) => {
        totalPrice += product.discount_price || product.actual_price; // Подсчет общей стоимости
        const card = createCard(product);
        container.appendChild(card);
    });

    // Добавляем обработчики для даты и времени доставки
    const deliveryDateInput = document.getElementById('delivery_date');
    const deliveryTimeInput = document.getElementById('delivery-time');
    
    function calculateDeliveryPrice() {
        let deliveryPrice = 200; // Базовая стоимость

        if (deliveryDateInput.value && deliveryTimeInput.value) {
            const selectedDate = new Date(deliveryDateInput.value);
            const dayOfWeek = selectedDate.getDay();
            const selectedTime = deliveryTimeInput.value;

            // Проверяем выходные (суббота - 6, воскресенье - 0)
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                deliveryPrice += 300;
            }

            // Проверяем вечернее время
            if (selectedTime === "18:00-22:00") {
                deliveryPrice += 200;
            }
        }

        return deliveryPrice;
    }

    function updateTotalPrice() {
        const deliveryPrice = calculateDeliveryPrice();
        const finalPrice = totalPrice + deliveryPrice;
        
        // Обновляем отображение цен
        const totalPriceElement = document.querySelector('#total-price');
        totalPriceElement.innerHTML = `
            Стоимость товаров: ${totalPrice} ₽<br>
            Стоимость доставки: ${deliveryPrice} ₽<br>
            <strong>Итого: ${finalPrice} ₽</strong>
        `;
    }

    // Добавляем слушатели событий
    if (deliveryDateInput && deliveryTimeInput) {
        deliveryDateInput.addEventListener('change', updateTotalPrice);
        deliveryTimeInput.addEventListener('change', updateTotalPrice);
    }

    // Инициализируем отображение цены
    updateTotalPrice();
}
document.addEventListener('DOMContentLoaded', () => {
    const resetButton = document.querySelector('button[type="button"]');

    resetButton.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('cart');
        const form = document.querySelector('form');
        form.reset();
        const deliveryDateInput = document.getElementById('delivery_date');
        const deliveryTimeInput = document.getElementById('delivery-time');
        if (deliveryDateInput) deliveryDateInput.value = '';
        if (deliveryTimeInput) deliveryTimeInput.value = '';
        const commentTextarea = document.getElementById('comment');
        if (commentTextarea) commentTextarea.value = '';
        const subscribeCheckbox = document.getElementById('subscribe');
        if (subscribeCheckbox) subscribeCheckbox.checked = true;
        const productsContainer = document.getElementById('productsContainer');
        if (productsContainer) productsContainer.innerHTML = '';
        const totalPriceElement = document.querySelector('#total-price');
        if (totalPriceElement) {
            totalPriceElement.innerHTML = `
                Стоимость товаров: 0 ₽<br>
                Стоимость доставки: 200 ₽<br>
                <strong>Итого: 200 ₽</strong>
            `;
        }
        displayNotification('Корзина очищена, форма сброшена');
        location.reload();
    });
});

function createCard(product) {
    const card = document.createElement("div");
    card.classList.add("card");

    const img = document.createElement("img");
    img.src = product.image_url;
    card.appendChild(img);

    const infoDiv = document.createElement("div");
    card.appendChild(infoDiv);

    const priceDiv = document.createElement("div");
    infoDiv.appendChild(priceDiv);
    if (product.discount_price !== null) {
        const discountPrice = document.createElement("p");
        discountPrice.classList.add("newPrice");
        discountPrice.textContent = `${product.discount_price} ₽`;
        priceDiv.appendChild(discountPrice);

        const price = document.createElement("p");
        price.classList.add("oldPrice");
        price.textContent = `${product.actual_price} ₽`;
        priceDiv.appendChild(price);

        const discountPercent = document.createElement("p");
        discountPercent.classList.add("discountPercent");
        discountPercent.textContent = `${-Math.round((1 - product.discount_price / product.actual_price) * 100)}%`;
        priceDiv.appendChild(discountPercent);
    } else {
        const price = document.createElement("p");
        price.classList.add("newPrice");
        price.textContent = `${product.actual_price} ₽`;
        priceDiv.appendChild(price);
    }

    const productRating = document.createElement("p");
    productRating.classList.add("rating");
    productRating.textContent = `Рейтинг: ${product.rating}`;
    infoDiv.appendChild(productRating);

    const title = document.createElement("h2");
    title.textContent = product.name;
    infoDiv.appendChild(title);

    const button = document.createElement("button");
    const handleProductClick = () => removeCartElement(product.id); // Изменено: удаление товара из корзины
    button.addEventListener('click', handleProductClick);
    button.textContent = "Удалить из корзины"; // Изменен текст кнопки
    infoDiv.appendChild(button);

    return card;
}

async function removeCartElement(id) {
    let cart = getCartItems();
    if (cart.includes(id)) {
        cart = cart.filter(itemId => itemId !== id);
        localStorage.setItem('cart', JSON.stringify(cart));
        location.reload(); // Обновляем страницу, чтобы отобразить изменения
    } else {
        console.log(`Товар с ID ${id} не найден в корзине.`);
    }
}

// Функция для добавления товара в корзину
function addToCart(product) {
    let cart = getCartItems();
    if (!cart.includes(product.id)) {
        cart.push(product.id);
        localStorage.setItem('cart', JSON.stringify(cart));
        displayNotification('Товар добавлен в корзину!');
    } else {
        displayNotification('Этот товар уже в корзине!');
    }
}

async function submitOrder(e) {
    e.preventDefault();
    const form = document.getElementById('order-form');
    const formData = new FormData(form);
    const productIds = await getCartItems();
    productIds.forEach(async (id) => {
        formData.append('good_ids', id);
    });
    const deliveryDateInput = document.getElementById('delivery_date');
    if (!deliveryDateInput || !deliveryDateInput.value) {
        console.error("Поле 'delivery_date' отсутствует или пустое");
        return;
    }
    
    const subscribeInput = document.getElementById('subscribe');
    const subscribeValue = subscribeInput && subscribeInput.value === 'on' ? true : false;
    
    formData.set('delivery_date', formatDate(deliveryDateInput.value));
    formData.set('subscribe', subscribeValue);
    
    for (let pair of formData.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`);
    }
    const response = await fetch('https://edu.std-900.ist.mospolytech.ru/exam-2024-1/api/orders?api_key=e8edbd36-da5f-4862-bda5-06eeb0c60a19', {
        method: 'POST',
        body: formData
    });
    if (response.status === 200) {
        await displayNotification('Заказ успешно оформлен');
        setTimeout(onOrderAccess, 3000);
    } else {
        await displayNotification('Ошибка оформления заказа');
    }
}

async function onOrderAccess() {
    window.localStorage.removeItem('cart');
    location.replace('index.html');
}


async function displayNotification(message) {
    const notificationContainer = document.getElementById('notification-container');
    notificationContainer.style.display = 'block';

    const notification = document.createElement('div');
    const notificationMessage = document.createElement('p');
    notificationMessage.textContent = message;
    notification.appendChild(notificationMessage);

    const notificationButton = document.createElement('button');
    const buttonImg = document.createElement('img');
    buttonImg.src = 'images/close.svg';
    notificationButton.appendChild(buttonImg);
    notificationButton.addEventListener('click', function () {
        notification.parentNode.removeChild(notification);
        if (notificationContainer.innerHTML === '') {
            notificationContainer.display = 'none';
        }
    });
    notification.appendChild(notificationButton);
    notificationContainer.appendChild(notification);
}

function formatDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}.${month}.${year}`;
}

async function displayNotification(message) {
    const notificationContainer = document.getElementById('notification-container');
    notificationContainer.style.display = 'block';

    const notification = document.createElement('div');
    const notificationMessage = document.createElement('p');
    notificationMessage.textContent = message;
    notification.appendChild(notificationMessage);

    const notificationButton = document.createElement('button');
    notificationButton.innerHTML = 'Окей <span>&#128076;</span>';
    notificationButton.addEventListener('click', function () {
        notification.parentNode.removeChild(notification);
        if (notificationContainer.innerHTML === '') {
            notificationContainer.display = 'none';
        }
    });
    notification.appendChild(notificationButton);
    notificationContainer.appendChild(notification);
}