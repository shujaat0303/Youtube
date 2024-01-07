// Function to toggle between subscribing and unsubscribing
function subscribeForm() {
    if ($('#subscribe-btn').hasClass('subscribed')) {
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
    $.ajax({
        url: $('#subscribeForm').attr('action'),
        type: 'POST',
        data: $('#subscribeForm').serialize(),
        success: function(response) {
            handleUnsubscribeResponse(response);
        },
        error: function(error) {
            // Handle error
            console.log(error);
        }
    });
}

// Function to handle the response after a successful subscribe/unsubscribe
function handleSubscribeResponse(response) {
    if (response.success) {
        var button = $('#subscribe-btn');
        button.text('SUBSCRIBED');
        button.addClass('subscribed');
    } else {
        // Handle failure if needed
        console.log('Subscription failed');
    }
}

// Corrected function to handle the response after a successful unsubscribe
function handleUnsubscribeResponse(response) {
    if (response.success) {
        var button = $('#subscribe-btn');
        button.text('SUBSCRIBE');
        button.removeClass('subscribed');
    } else {
        // Handle failure if needed
        console.log('Unsubscription failed');
    }
}
