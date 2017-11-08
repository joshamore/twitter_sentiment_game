// Stores temporary data
var model = {
    // Stores polarity data for chart
    polarityData: 0
};


// Logical functions and backend requests
var controller = {
    // Pulls polarity via get request and stores in model for use in chart
    tweetData: function(callback) {
        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/twitterdata',
            data: {username: document.querySelector("#twitterUsername").textContent},
            success: function(results) {
                returnData = [];
                
                // Stores sentiment data in correct order inside an array
                returnData.push(results.positive);
                returnData.push(results.neutral);
                returnData.push(results.negative);
                
                // Sets model polarityData to complete array
                model.polarityData = returnData;
                
                // Returns passed callback function
                return callback()
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
        // This function will be called from inside tweetData function as callback
        function generateChart() {
            // Inserts chart canvas into DOM
            $('#resultsVisData').html('<canvas id="myChart" width="400" height="400"></canvas>');
            // Creating chart with model data
            controller.chart();
        }
        
        // Pulling Tweet data and generating the chart after receiving data
        controller.tweetData(generateChart);
    })
};
