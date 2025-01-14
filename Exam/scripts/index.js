
document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('sort_order').addEventListener('change', async () => {
        const url = new URL(window.location);
        url.searchParams.set('sort_order', document.getElementById('sort_order').value);
        window.history.pushState({}, '', url);
        location.reload();
    });
    const urlParams = new URLSearchParams(window.location.search);
    const sortOrder = urlParams.get('sort_order') ? urlParams.get('sort_order') : 'rating_desc';
    document.getElementById('sort_order').value = sortOrder;
    
    let products = await fetch(`https://edu.std-900.ist.mospolytech.ru/exam-2024-1/api/goods?api_key=e8edbd36-da5f-4862-bda5-06eeb0c60a19&page=1&per_page=97&sort_order=${sortOrder}`);
    products = (await products.json())["goods"];

    populateCards(products);


    function populateCards(products) {
        const container = document.getElementById("productsContainer");
        container.innerHTML = '';
        products.forEach((product) => {
            const card = createCard(product);
            container.appendChild(card);
        });
    }

 

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
        const handleProductClick = () => addToCart(product);
        button.addEventListener(`click`, handleProductClick);
        button.textContent = "Добавить";
        infoDiv.appendChild(button);

        return card;
    }

    function addToCart(product) {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        if (!cart.includes(product.id)) {
            cart.push(product.id);
            localStorage.setItem('cart', JSON.stringify(cart));
            displayNotification(`Продукт "${product.name}" добавлен в корзину.`);
        }
    }
    function getCartItems() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }

    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const autocompleteList = document.getElementById('autocompleteList');

    // Функция для получения списка автозаполнения с учётом текущего запроса
    async function fetchAutocompleteData(query) {
        const apiUrl = `https://edu.std-900.ist.mospolytech.ru/exam-2024-1/api/autocomplete?api_key=e8edbd36-da5f-4862-bda5-06eeb0c60a19&query=${encodeURIComponent(query)}`;
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error('Ошибка при получении данных с API');
            }
            return await response.json();
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
            return [];
        }
    }

    // Функция для отображения поисковых подсказок
    async function showAutocompleteSuggestions() {
        const query = searchInput.value.trim();
        if (!query) {
            autocompleteList.classList.add('hidden');
            autocompleteList.innerHTML = ''; // Очищаем список
            return;
        }

        const suggestions = await fetchAutocompleteData(query);

        if (suggestions.length === 0) {
            autocompleteList.classList.add('hidden');
            autocompleteList.innerHTML = ''; // Очищаем список
            return;
        }

        // Генерация списка подсказок
        autocompleteList.innerHTML = '';
        suggestions.forEach(suggestion => {
            const listItem = document.createElement('li');
            listItem.textContent = suggestion;
            listItem.classList.add('autocomplete-item');

            // При клике на подсказку — подставляем её в поле ввода
            listItem.addEventListener('click', () => {
                searchInput.value = suggestion;
                autocompleteList.classList.add('hidden');
            });

            autocompleteList.appendChild(listItem);
        });

        autocompleteList.classList.remove('hidden');
    }

    // Обработчик ввода текста в строку поиска
    searchInput.addEventListener('input', async () => {
        await showAutocompleteSuggestions();
    });

    // Обработчик клика по кнопке "Найти"
    searchButton.addEventListener('click', (event) => {
        event.preventDefault();
        
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {
            displayNotification('Введите текст для поиска!');
            return;
        }
        
        const filteredProducts = filterProductsBySearch(products, query);
        console.log(filteredProducts);
        populateCards(filteredProducts);
        
        autocompleteList.classList.add('hidden');
        autocompleteList.innerHTML = '';
    });

    // Закрытие подсказок при клике вне области поиска
    document.addEventListener('click', (event) => {
        const targetElement = event.target;
        if (!targetElement.closest('#searchTextBut') && targetElement !== searchInput) {
            autocompleteList.classList.add('hidden');
        }
    });

    /**
     * Демонстрационные функции, которые нужно заменить своими.
     * Здесь лишь имитация функциональности:
     */

    // Пример: фильтруем список товаров
    function filterProductsBySearch(products, query) {
        return products.filter(product => product.name.toLowerCase().includes(query));
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
});