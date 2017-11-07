// CHART TEST
function chart() {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}
/*ALL THE BELOW WILL BE DELETED -- NO LONGER BEING USED */

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
    }),
    resultClick: $('#resultArea').click(function() {
        $('#resultArea').html('<canvas id="myChart" width="400" height="400"></canvas>');
        chart();
    })
};
