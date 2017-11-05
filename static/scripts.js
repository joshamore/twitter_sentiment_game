// Stores required temporary data
var model = {
    guess: null
};


// Methods that communicate with the server
var controller = {
    guessClick: function() {
        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/twitterdata',
            data: {username: document.querySelector("#username").textContent, guess: model.guess},
            success: function(results) {
                console.log(results);
            }
        });
    }
};


// Triggers based on user interactions
var events = {
    positiveClick: $('#positive').click(function() {
        model.guess = 'positive';
        controller.guessClick();
    }),
    positiveClick: $('#negative').click(function() {
        model.guess = 'negative';
        controller.guessClick();
    })
};