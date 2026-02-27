function submitOrder() {
    const customerName = document.getElementById("customerNameInput");
    const address = document.getElementById("deliveryAddressInput");
    
    const request_data = {
        client_id: user,
        customer_name: customerName.value,
        delivery_address: address.value
    };

    try {
        fetch('http://localhost:8004/orders', {
            method: "POST",
            body: JSON.stringify(request_data),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.message == "Order received"){
                customerName.value = "";
                address.value = "";
                hidePopup("newOrderSection");
            } else {
                alert("Failed to submit order. Please try again.");
                console.error("Order submission failed:", data);
            }
        })
        .catch(error => {
            console.error("Error submitting order:", error);
            alert("An error occurred while submitting your order. Please try again.");
        });
    } catch (error) {
        console.error("Unexpected error:", error);
        alert("An unexpected error occurred. Please try again.");
    }
}

function updateOrderTable(){
    fetch('http://localhost:8003/client_orders/' + user)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("orderTable");
            tableBody.innerHTML = "";
            const headRow = document.createElement("tr");
            headRow.innerHTML = `
                <th>Order ID</th>
                <th>Customer Name</th>
                <th>Delivery Address</th>
                <th>Status</th>
            `;
            tableBody.appendChild(headRow);
            console.log("Received orders data:", data.Order);
        })
        .catch(error => {
            console.error("Error updating order table:", error);
        });
}
