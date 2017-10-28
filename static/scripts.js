// Stores the prefix to the root application folder
// TODO: Update this with dynamic Flask address
$SCRIPT_ROOT = "http://127.0.0.1:5000";


// TESTING -- This ajax request retrieves data from backend and logs data to the console.
$('.btn').click(function() {
    $.ajax({
        type: 'GET',
        url: $SCRIPT_ROOT + '/test',
        data: {username: document.querySelector("#username").textContent},
        success: function(results) {
            console.log(results);
            
            $("#test").append(results)
        }
    });
});