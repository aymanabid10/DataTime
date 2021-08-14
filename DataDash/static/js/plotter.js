data = [];
labels = [];
var ctx = $("#myChart");
$(document).ready(function(){

    function addData(chart, label, data) {
        chart.data.labels=label;
        chart.data.datasets.forEach((dataset) => {
            dataset.data = data ;
        });

        chart.update();
    };
    
    function removeData(chart) {
        chart.data.labels.pop();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
        });

        chart.update();
    };

    function UpdateData(){

        var requests = $.get('/data_json');
    
        var tm = requests.done(function (result)
        {
            data = result["data"];
            labels = result["labels"];
            removeData(myChart);
            addData(myChart,labels,data);
        });
    };

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Number of Samples found or Collected',
                data: [],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive : true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    setInterval(UpdateData,2000)
});