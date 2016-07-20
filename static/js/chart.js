var myListener;
var sampleData;
$(function() {
    function makeChart(container, labels, name, description, color) {
        return new Highcharts.Chart({
            chart: {
                renderTo: container,
                type: 'column',
            },
            color: color,
            title: { text: name + ' demographics' + description },
            legend: { enabled: false },
            xAxis: {
                categories: labels,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Number of people',
                },
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            credits: { enabled: false },
            series: [{ data: [2, 3], color: color}]
        });
    }
    disagree = ' of people who disagree with you';
    inMap = ' of people in the current map area';
    c1 = '#ff7f0e';
    c2 = '#1f77b4';
    genderChart = makeChart('genderContainerMap', ['Female', 'Male'], 'Gender', inMap, c1);
    nationalityChart = makeChart('nationalityContainerMap', ['Palestinian', 'Israeli'], 'Nationality', inMap, c1);
    genderChartDisagree = makeChart('genderContainerDisagree', ['Female', 'Male'], 'Gender', disagree, c2);
    nationalityChartDisagree = makeChart('nationalityContainerDisagree', ['Palestinian', 'Israeli'], 'Nationality', disagree, c2);

    $.get("get_disagreement_demographics", function(json) {
        genderChartDisagree.series[0].setData([json['gender']['Female'], json['gender']['Male']] );
        nationalityChartDisagree.series[0].setData([json['nationality']['Palestinian'], json['nationality']['Israeli']] );
    });

    myListener = function(data) {
        $.get("get_map_demographics", data, function(json) {
            genderChartMap.series[0].setData([json['gender']['Female'], json['gender']['Male']] );
            nationalityChartMap.series[0].setData([json['nationality']['Palestinian'], json['nationality']['Israeli']] );
        });
    };
    sampleData = {'lat_start': 31.764, 'lat_end': 32, 'lon_start': 35.22, 'lon_end': 36.};
});

