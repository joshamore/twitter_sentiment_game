// Stores the prefix to the root application folder
// TODO: Update this with dynamic Flask address
$SCRIPT_ROOT = "http://127.0.0.1:5000";


// FOR TESTING.
// TODO: Update functionality so guess data is sent to server with GET request.
var model = {
    guess: null
};


// Communicates with server
// TODO: Clean up JS ajax request -- consider using MVC-esque seperation. Example in JS calculator project.
var controller = {
    guessClick: function() {
        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/twitterdata',
            data: {username: document.querySelector("#username").textContent, guess: model.guess},
            success: function(results) {
                console.log(results);
                
                $("#test").append(results.results)
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