function sendMessage() {
    var inputMessage = document.getElementById('inputMessage');
    var message = inputMessage.value.trim();
    if (message !== '') {
        var chatBox = document.getElementById('chatBox');
        var userMessage = '<div class="user-message">' + message + '</div>';
        chatBox.innerHTML += userMessage;

        // Clear input field
        inputMessage.value = '';

        // Scroll to bottom of chat box
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send message to Flask server for classification
        classifyExpense(message);
    }
}

function classifyExpense(message) {
    // Prepare the request data
    var requestData = { "text": message };

    // Send POST request to Flask server
    fetch('http://127.0.0.1:5000/classify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Simulate typing animation
        var typingInterval = 50; // Interval between each character (in milliseconds)
        var botMessage = 'Expense of ' + data.expense + ' Rs on ' + data.predicted_label + ' logged';
        var chatBox = document.getElementById('chatBox');
        var userMessage = chatBox.lastElementChild; // Get the last user message

        // Display the bot's response message below the user message
        var botMessageElement = document.createElement('div');
        botMessageElement.className = 'bot-message';
        botMessageElement.innerText = botMessage;
        userMessage.insertAdjacentElement('afterend', botMessageElement);

        // Scroll to bottom of chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}
