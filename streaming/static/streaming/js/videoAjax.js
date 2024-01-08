

// Function to toggle between subscribing and unsubscribing
function subscribeForm() {
    if ($('#video-subscribe-btn').hasClass('subscribed')) {
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
        var button = $('#video-subscribe-btn');
        button.text('Subscribed');
        button.addClass('subscribed');
    } else {
        // Handle failure if needed
        console.log('Subscription failed');
    }
}

// Corrected function to handle the response after a successful unsubscribe
function handleUnsubscribeResponse(response) {
    if (response.success) {
        var button = $('#video-subscribe-btn');
        button.text('Subscribe');
        button.removeClass('subscribed');
    } else {
        // Handle failure if needed
        console.log('Unsubscription failed');
    }
}

//________________________________________________________________________________________________
//Like button
// Function to toggle between subscribing and unsubscribing
function likeForm() {
    if ($('#like-btn').hasClass('liked')) {
        // If already subscribed, initiate the unsubscribe process
        unlike();
    } else {
        // If not subscribed, initiate the subscribe process
        like();
    }
}

// Function to handle the subscribe process
function like() {
    $.ajax({
        url: $('#likeForm').attr('action'),
        type: 'POST',
        data: $('#likeForm').serialize(),
        success: function(response) {
            handleLikeResponse(response);
        },
        error: function(error) {
            // Handle error
            console.log(error);
        }
    });
}

// Function to handle the unsubscribe process
function unlike() {
    $.ajax({
        url: $('#likeForm').attr('action'),
        type: 'POST',
        data: $('#likeForm').serialize(),
        success: function(response) {
            handleUnlikeResponse(response);
        },
        error: function(error) {
            // Handle error
            console.log(error);
        }
    });
}

// Function to handle the response after a successful subscribe/unsubscribe
function handleLikeResponse(response) {
    if (response.success) {
        var button = $('#like-btn');
        button.addClass('liked');
    } else {
        // Handle failure if needed
        console.log('like failed');
    }
}

// Corrected function to handle the response after a successful unsubscribe
function handleUnlikeResponse(response) {
    if (response.success) {
        var button = $('#like-btn');
        button.removeClass('liked');
    } else {
        // Handle failure if needed
        console.log('Unlike failed');
    }
}

//________________________________________________________________________________________________
//Comment button
function commentForm(){
    $('#commentForm').submit(function (e) {
        e.preventDefault();
        data=$('#commentForm').serialize();
        $('#id_comment').val('');
        $.ajax({
            type: 'POST',
            url: $('#comment_url').attr('href'),
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    // Handle success, for example, update the UI
                    console.log('Comment added successfully');

                    $('#old-comments-box').prepend(response.comment_html);
                    // You can update the UI here as needed
                } else {
                    // Handle errors, for example, display validation errors
                    console.error('Error adding comment:', response.errors);
                    // You can display validation errors or take other actions
                }
            },
            error: function () {
                console.error('Error submitting comment');
            }
        });
    });
}