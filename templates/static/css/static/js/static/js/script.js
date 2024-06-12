// Add event listeners to the order form
document.getElementById('order-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    const currency = document.getElementById('currency').value;
    const price = document.getElementById('price').value;
    // Send the form data to the server
    fetch('/orders/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            amount,
            currency,
            price
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Order was successful, display a success message
            alert('Order created successfully');
        } else {
            // Order failed, display an error message
            alert('Failed to create order');
        }
    });
});

// Add event listeners to the transaction form
document.getElementById('transaction-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    const currency = document.getElementById('currency').value;
    // Send the form data to the server
    fetch('/transactions/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            amount,
            currency
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Transaction was successful, display a success message
            alert('Transaction created successfully');
        } else {
            // Transaction failed, display an error message
            alert('Failed to create transaction');
        }
    });
});
