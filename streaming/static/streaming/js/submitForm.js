function submitForm(formId) {
    $.ajax({
        url: $('#' + formId).attr('action'),
        type: 'POST',
        data: $('#' + formId).serialize(),
        success: function(response) {
            // Handle success, e.g., update UI dynamically
            handleSubscribeResponse(response);
            console.log(response);
        },
        error: function(error) {
            // Handle error
            console.log(error);
        }
    });
}



// Function to toggle between subscribing and unsubscribing
function toggleSubscription() {
    if (isSubscribed) {
        // If already subscribed, initiate the unsubscribe process
        unsubscribe();
    } else {
        // If not subscribed, initiate the subscribe process
        subscribe();
    }
}

// Function to handle the subscribe process
function subscribe() {
    $.ajax({
        url: $('#subscribeForm').attr('action'),
        type: 'POST',
        data: $('#subscribeForm').serialize(),
        success: function(response) {
            handleSubscribeResponse(response);
        },
        error: function(error) {
            // Handle error
            console.log(error);
        }
    });
}

// Function to handle the unsubscribe process
function unsubscribe() {
    // Implement the AJAX logic for unsubscribing (similar to the subscribe function)
    // ...

    // For demo purposes, I'm just toggling the subscription state without an actual AJAX call
    handleUnsubscribeResponse({ success: true });
}

// Function to handle the response after a successful subscribe/unsubscribe
function handleSubscribeResponse(response) {
    if (response.success) {
        isSubscribed = true;
        updateButtonState();
    } else {
        // Handle failure if needed
        console.log('Subscription failed');
    }
}

// Function to handle the response after a successful unsubscribe
function handleUnsubscribeResponse(response) {
    if (response.success) {
        isSubscribed = false;
        updateButtonState();
    } else {
        // Handle failure if needed
        console.log('Unsubscription failed');
    }
}

// Function to update the button state based on the subscription status
function updateButtonState() {
    var button = $('#video-subscribe-btn');
    if (isSubscribed) {
        button.text('Unsubscribe');
        button.addClass('subscribed');
    } else {
        button.text('Subscribe');
        button.removeClass('subscribed');
    }
}
