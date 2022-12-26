
$('#view-chart').click(function(){
    date_start = $('#date-start').text()
    date_end = $('#date-end').text()
    console.log(date_start,date_end)
    $.ajax({
        type:'POST',
        url:"/store/getvaluechart/",
        contentType: "json",
        data:JSON.stringify({
            post:true,
            date_start : date_start,
            date_end  : date_end
        }),
        success:function(response){
            x=[]
            y=[]
            for (item of JSON.parse(response)){
                year = parseInt(item.x.split("-")[0].replace('"',""))
                month = parseInt(item.x.split("-")[1])
                day = parseInt(item.x.split("-")[2].split(" ")[0])
                hours = parseInt(item.x.split("-")[2].split(" ")[1].split(":")[0])
                minutes = parseInt( item.x.split("-")[2].split(" ")[1].split(":")[1])
                seconds = parseFloat(item.x.split("-")[2].split(" ")[1].split(":")[2].split('+')[0])
                date = new Date(year, month, day, hours, minutes, seconds);
                x.push(date)
                y.push(parseFloat(item.y))
            }
            $('.char-area').append("<canvas id='myChart'></canvas>")
            chart = new Chart("myChart", {
                type: "line",
                data: {
                  labels: x,
                  datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "rgba(0,0,255,0.2)",
                    color: "black",
                    data: y
                  }]
                },
                options: {
                  legend: {display: true},
                  scales: {
                    yAxes: [{ticks: {min: 0, max:Math.max( ...y ) + Math.min( ...y ) }}],
                  },
                  color: "red"
                }
              });
        }
    })
})
