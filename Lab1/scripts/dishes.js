document.addEventListener('DOMContentLoaded', () => {
    fetch('dishes.json')
        .then(response => response.json())
        .then(data => {
            // Сортировка
            const sortedDishes = data['dishes'].sort((a, b) => {
                return a['name'].localeCompare(b['name'], 'ru');
            });

            // Блюда
            const soupSection = document.querySelectorAll('#soup .dish_block')[0];
            const mainDishSection = document.querySelectorAll('#main .dish_block')[0];
            const drinkSection = document.querySelectorAll('#drink .dish_block')[0];
            const saladSection = document.querySelectorAll('#salad .dish_block')[0];
            const dessertSection = document.querySelectorAll('#dessert .dish_block')[0];

            function createCard(dish) {
                const card = document.createElement('div');
                card.classList.add('dish');
                card.dataset.kind = dish['kind'];

                const img = document.createElement('img');
                img.src = dish['image'];
                img.alt = dish['name'];

                const price = document.createElement('p');
                price.classList.add('price');
                price.textContent = dish['price'] + '₽';

                const dishName = document.createElement('p');
                dishName.classList.add('dish_name');
                dishName.textContent = dish['name'];

                const volume = document.createElement('p');
                volume.classList.add('volume');
                volume.textContent = dish['volume'];

                const buttonDiv = document.createElement('div');
                const button = document.createElement('button');
                button.textContent = 'Добавить';
                buttonDiv.appendChild(button);

                card.appendChild(img);
                card.appendChild(price);
                card.appendChild(dishName);
                card.appendChild(volume);
                card.appendChild(buttonDiv);

                button.addEventListener('click', () => {
                    addToOrder(dish);
                });

                return card;
            }

            function populateCards(sectionElement, category) {
                sortedDishes.forEach(dish => {
                    if (dish['category'] === category) {
                        const card = createCard(dish);
                        sectionElement.appendChild(card);
                    }
                });
            }
            populateCards(soupSection, 'суп');
            populateCards(mainDishSection, 'главное блюдо');
            populateCards(drinkSection, 'напиток');
            populateCards(saladSection, 'салат');
            populateCards(dessertSection, 'десерт');

            // Добавление товаров и цены
            let totalPrice = 0;
            const totalPriceElement = document.getElementById('total_price');

            let selectedDishes = {
                'суп': null,
                'главное блюдо': null,
                'напиток': null,
                'салат': null,
                'десерт': null
            };

            const chosenSoup = document.getElementById('chosen_soup');
            const chosenMain = document.getElementById('chosen_main');
            const chosenDrink = document.getElementById('chosen_drink');
            const chosenSalad = document.getElementById('chosen_salad');
            const chosenDessert = document.getElementById('chosen_dessert');
            const soupLabel = document.getElementById('soup_label');
            const mainLabel = document.getElementById('main_label');
            const drinkLabel = document.getElementById('drink_label');
            const saladLabel = document.getElementById('salad_label');
            const dessertLabel = document.getElementById('dessert_label');
            const nothingSelectedMessage = document.querySelector('.order_section p:nth-of-type(2)');


            soupLabel.style.display = 'none';
            chosenSoup.style.display = 'none';
            mainLabel.style.display = 'none';
            chosenMain.style.display = 'none';
            drinkLabel.style.display = 'none';
            chosenDrink.style.display = 'none';
            saladLabel.style.display = 'none';
            chosenSalad.style.display = 'none';
            dessertLabel.style.display = 'none';
            chosenDessert.style.display = 'none';
            totalPriceElement.style.display = 'none';

            function addToOrder(dish) {
                let isUpdated = false;

                if (dish['category'] === 'суп') {
                    updateCategory('суп', dish, chosenSoup, soupLabel);
                    isUpdated = true;
                } else if (dish['category'] === 'главное блюдо') {
                    updateCategory('главное блюдо', dish, chosenMain, mainLabel);
                    isUpdated = true;
                } else if (dish['category'] === 'напиток') {
                    updateCategory('напиток', dish, chosenDrink, drinkLabel);
                    isUpdated = true;
                } else if (dish['category'] === 'салат') {
                    updateCategory('салат', dish, chosenSalad, saladLabel);
                    isUpdated = true;
                } else if (dish['category'] === 'десерт') {
                    updateCategory('десерт', dish, chosenDessert, dessertLabel);
                    isUpdated = true;
                }

                if (isUpdated) {
                    nothingSelectedMessage.style.display = 'none';
                }

                totalPriceElement.textContent = `Стоимость заказа: ${totalPrice}₽`;
                totalPriceElement.style.display = 'block';

                showEmptyCategories();
            }

        function updateCategory(category, dish, chosenElement, labelElement) {
                // Если удаляем блюдо, то вычитаем цену
                if (selectedDishes[category] !== null) {
                    totalPrice -= selectedDishes[category]['price'];
                }

                // Выбранное блюдо меняется
                selectedDishes[category] = dish;
                chosenElement.textContent = `${dish['name']} ${dish['price']}₽`;
                chosenElement.style.display = 'block';
                labelElement.style.display = 'block';

                // Цена выбранного блюда
                totalPrice += dish['price'];
            }

            // Показываем пустые категории
            function showEmptyCategories() {
                if (selectedDishes['суп'] === null) {
                    chosenSoup.textContent = 'Блюдо не выбрано';
                    soupLabel.style.display = 'block';
                    chosenSoup.style.display = 'block';
                }
                if (selectedDishes['главное блюдо'] === null) {
                    chosenMain.textContent = 'Блюдо не выбрано';
                    mainLabel.style.display = 'block';
                    chosenMain.style.display = 'block';
                }
                if (selectedDishes['напиток'] === null) {
                    chosenDrink.textContent = 'Блюдо не выбрано';
                    drinkLabel.style.display = 'block';
                    chosenDrink.style.display = 'block';
                }
                if (selectedDishes['салат'] === null) {
                    chosenSalad.textContent = 'Блюдо не выбрано';
                    saladLabel.style.display = 'block';
                    chosenSalad.style.display = 'block';
                }
                if (selectedDishes['десерт'] === null) {
                    chosenDessert.textContent = 'Блюдо не выбрано';
                    dessertLabel.style.display = 'block';
                    chosenDessert.style.display = 'block';
                }
            }

            const soupFilters = document.querySelectorAll('.soup-filter');
            const mainFilters = document.querySelectorAll('.main-filter');
            const drinkFilters = document.querySelectorAll('.drink-filter');
            const saladFilters = document.querySelectorAll('.salad-filter');
            const dessertFilters = document.querySelectorAll('.dessert-filter');

            function addFiltersToCategory(filters) {
                filters.forEach(filter => {
                    filter.addEventListener('click', function(e) {
                        e.preventDefault();

                        const className = filter.classList[0].split('-')[0];
                        const dishes = document.querySelectorAll(`#${className} .dish`);

                        if (!filter.classList.contains('active')) {
                            filters.forEach(f => f.classList.remove('active'));
                            filter.classList.add('active');
                            const kind = filter.dataset.kind;
                            dishes.forEach(dish => {
                                if (dish.dataset.kind === kind) {
                                    dish.classList.remove('hidden');
                                } else {
                                    dish.classList.add('hidden');
                                }
                            });
                        } else {
                            filter.classList.remove('active');
                            dishes.forEach(dish => dish.classList.remove('hidden'));
                        }
                    });
                });
            }

            addFiltersToCategory(soupFilters);
            addFiltersToCategory(mainFilters);
            addFiltersToCategory(saladFilters);
            addFiltersToCategory(drinkFilters);
            addFiltersToCategory(dessertFilters);
        });
});