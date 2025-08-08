function searchProducts() {
    const query = document.getElementById("searchBox").value;
    fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    })
    .then(res => res.json())
    .then(data => {
        displayProducts(data, "products");
    });
}

function getRecommendations(id) {
    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        displayProducts(data, "recList");
    });
}

function displayProducts(products, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";
    products.forEach(p => {
        const div = document.createElement("div");
        div.className = "product";
        div.innerHTML = `
            <h3>${p.name}</h3>
            <p>${p.description}</p>
            <p><strong>Price:</strong> $${p.price}</p>
            <p><strong>Category:</strong> ${p.category}</p>
            <p><strong>Rating:</strong> ${p.rating}</p>
            <button onclick="getRecommendations(${p.id})">Recommend Similar</button>
        `;
        container.appendChild(div);
    });
}
