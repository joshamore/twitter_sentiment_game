// Stores temporary data
var model = {
    // Polarity data for results chart
    polarityData: 0,
    // History data for history chart
    historyData: 0,
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
    resultsChart: function() {
        var ctx = document.getElementById("resultsChart").getContext('2d');
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
    },
    historyData: function(callback) {
        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/historyguessdata',
            success: function(results) {
                model.historyData = results;
                
                return callback()
            }
        });
    },
    historyChart: function() {
        var ctx = document.getElementById("historyChart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            cutoutPercentage: 50,
            data: {
                labels: ["Correct", "Incorrect"],
                datasets: [{
                    label: 'Correct vs. Incorrect Guesses',
                    data: model.historyData,
                    backgroundColor: [
                        '#50db1e',
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
    // Generates Twitter polarity chart and adds to DOM on click
    resultClick: $('#showVisData').click(function() {
        // This function will be called from inside tweetData function as callback when AJAX returns
        function generateChart() {
            // Inserts chart canvas into DOM
            $('#resultsVisData').html('<canvas id="resultsChart" width="400" height="400"></canvas>');
            
            // Creating chart with model data
            controller.resultsChart();
        }
        
        // Pulling Tweet data and generating the chart after receiving data
        controller.tweetData(generateChart);
    }),
    historyChartClick: $('#showHistoryChart').click(function() {
        // This function will be called from inside the historyData function as a callback when AJAX returns
        function generateChart() {
            // Inserts canvas into DOM
            $('#historyVisData').html('<canvas id="historyChart" width="400" height="400"</canvas>');
            
            // Creating chart with model data
            controller.historyChart();
        }
        
        // Pulling history data and generating chart after data is returned
        controller.historyData(generateChart);
    })
};