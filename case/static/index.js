document.addEventListener('click', function (event) {
    const dropdownContent = document.getElementById("dropdown-content");
    if (dropdownContent) {
        const isClickInside = dropdownContent.contains(event.target) || event.target.matches('.nav-link');
        if (!isClickInside) {
            dropdownContent.style.display = "none";
        }
    }
});

function toggleDropdown(event) {
    event.preventDefault();
    const dropdownContent = document.getElementById("dropdown-content");
    if (dropdownContent) {
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    }
}


let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

function toggleFavorite(productName, productImage) {
    const existingIndex = favorites.findIndex(item => item.name === productName);

    if (existingIndex >= 0) {
        favorites.splice(existingIndex, 1);
        console.log(`${productName} удален из избранного.`);
    } else {
        favorites.push({ name: productName, image: productImage });
        console.log(`${productName} добавлен в избранное.`);
    }

    localStorage.setItem('favorites', JSON.stringify(favorites));
    showTemporaryMessage(existingIndex >= 0 ? 'Удален из избранного' : 'Добавлен в избранное');
}

function viewFavorites() {
    const favoritesSection = document.getElementById('favorites');
    const favoritesList = document.getElementById('favorites-list');

    favoritesList.innerHTML = '';  // Clear previous view

    if (favorites.length > 0) {
        favorites.forEach(item => {
            const favoriteItem = document.createElement('div');
            favoriteItem.classList.add('product');
            favoriteItem.innerHTML = `
                <img src="/static/${item.image}" alt="${item.name}">
                <h3>${item.name}</h3>
                <button onclick="removeFavorite('${item.name}')">Удалить из избранного</button>
            `;
            favoritesList.appendChild(favoriteItem);
        });
    } else {
        favoritesList.innerHTML = '<p>Избранное пусто</p>';
    }

    favoritesSection.style.display = 'block';
}


function removeFavorite(productName) {
    favorites = favorites.filter(item => item.name !== productName);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    viewFavorites();
    showTemporaryMessage('Удален из избранного');
}

function showTemporaryMessage(message) {
    const msg = document.createElement('div');
    msg.className = 'cart-message';
    msg.textContent = message;
    document.body.appendChild(msg);

    setTimeout(() => msg.remove(), 3000);
}
