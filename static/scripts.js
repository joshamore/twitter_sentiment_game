// Stores required temporary data
var model = {
    // Stores polarity data for chart
    polarityData: 0
};


// Logical functions and backend requests
var controller = {
    // Pulls polarity via get request and stores in model for use in chart
    tweetData: function() {
        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/twitterdata',
            data: {username: document.querySelector("#twitterUsername").textContent},
            success: function(results) {
                returnData = [];
                
                returnData.push(results.positive);
                returnData.push(results.neutral);
                returnData.push(results.negative);
                
                model.polarityData = returnData;
            }
        });
    },
    chart: function() {
        var ctx = document.getElementById("myChart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            cutoutPercentage: 50,
            data: {
                labels: ["Positive", "Neutral", "Negative"],
                datasets: [{
                    label: 'Percentage of Sentiment',
                    data: model.polarityData,
                    backgroundColor: [
                        '#50db1e',
                        '#dddddd',
                        '#f23030'
                ]
                    }],
            },
            options: {

            }
        });
    }
};


// Triggers based on user interactions
var events = {
    // Generates Twitter polarity visual on click
    resultClick: $('#showVisData').click(function() {
        // Inserts chart canvas into DOM
        $('#resultsVisData').html('<canvas id="myChart" width="400" height="400"></canvas>');
        
        // Creating chart with model data
        controller.chart();
    }),
    // Makes get request for Twitter polarity data after DOM loads
    getPolarityData: document.addEventListener("DOMContentLoaded", function() {
        controller.tweetData();
    })
};
