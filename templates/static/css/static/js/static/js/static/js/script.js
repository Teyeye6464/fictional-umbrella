// Add event listeners to the socket.io events
socket.on('new_order', (data) => {
    // Display the new order
    alert(`New order created: ${data.amount} ${data.currency} @ ${data.price}`);
});

socket.on('new_transaction', (data) => {
    // Display the new transaction
    alert(`New transaction created: ${data.amount} ${data.currency}`);
});
