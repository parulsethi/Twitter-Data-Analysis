
	  
google.charts.load('current', {'packages':['corechart']});

server_url="http://127.0.0.1:2003"

// google.charts.setOnLoadCallback(global_chart);

cities=["Delhi","Mumbai"]
// function pieChart(data) {


// }




$("#retweet").click(function(){
	
	$.get(server_url+"/tweet/status",function(data){
		$("chart_id0").parent().html("<div id='chart_id0'></div>")
		$("#chart_id0").parent().append("<div id='chart_id1'></div>")
		tweets=data['retweets']

		for(var each_tweet=0;each_tweet<cities.length;each_tweet++){
			city=cities[each_tweet];
			var data=[];
			data[0]=["Tweets",city];
			data[1]=["Original_Tweets",(100-tweets[city])]
			data[2]=["ReTweets",tweets[city]]
			chart_d=google.visualization.arrayToDataTable(data)
			var options = {
			  title: 'Original Tweets- '+city
			};
			var chart = new google.visualization.PieChart(document.getElementById('chart_id'+each_tweet));
			chart.draw(chart_d, options);
		}

	});

});


$("#sentiment").click(function(){

$.get(server_url+"/tweet/sentiment",function(data){

		$("chart_id0").parent().html("<div id='chart_id0'></div>")

		var adata=[];
		adata[0]=["Sentiment Analysis ","#oddeven"];
		adata[1]=["Positive",(100*data['data']['+'])]
		adata[2]=["Negative",(100*data['data']['-'])]
		adata[3]=["Neutral",(100*data['data']['.'])]

		chart_d=google.visualization.arrayToDataTable(adata);
			var options = {
			  title: 'Sentiment Analysis of #oddeven'
			};
			var chart = new google.visualization.PieChart(document.getElementById('chart_id0'));
			chart.draw(chart_d, options);

	});


});



