
	  
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


$("#tweet_type").click(function(){

$.get(server_url+"/tweet/media_type",function(data){
		$("chart_id0").parent().html("<div id='chart_id0'></div>")
		$("#chart_id0").parent().append("<div id='chart_id1'></div>")
		tweets=data['data']

		for(var each_tweet=0;each_tweet<cities.length;each_tweet++){
			city=cities[each_tweet];
			var data=[];
			data[0]=["Tweets_Media",city];
			data[1]=["Media Only",tweets[city]['image']]
			data[2]=["Text Only",tweets[city]['text']]
			data[3]=["Text and Media",tweets[city]['text_image']]
			
			chart_d=google.visualization.arrayToDataTable(data)
			var options = {
			  title: 'Tweets Media Type- '+city
			};
			var chart = new google.visualization.PieChart(document.getElementById('chart_id'+each_tweet));
			chart.draw(chart_d, options);
		}

	});


});



$("#time_analysis").click(function(){

$.get(server_url+"/tweet/time",function(data){

		$("chart_id0").parent().html("<div id='chart_id0'></div>")
		data=data['data']
		console.log(data)
		data.unshift([ 'Season Start Date',"mumbai_rains","mumbai_cyclone","delhi_smog","delhi_myrightTobreathe","delhi_pollution","delhi_oddeven", 'Season End Date'])
		console.log(data)
		chart_d=google.visualization.arrayToDataTable(data);
			var options = {
			  title: 'Sentiment Analysis of #oddeven'
			};
			var chart = new google.visualization.LineChart(document.getElementById('chart_id0'));
			chart.draw(chart_d, options);

	});


});


$("#user_hist").click(function(){
$.get(server_url+"/user/histogram",function(data){

		$("chart_id0").parent().html("<div id='chart_id0'></div>")
		$("#chart_id0").parent().append("<div id='chart_id1'></div>")
		tweets=data['user_histogram']

		for(var each_tweet=0;each_tweet<cities.length;each_tweet++){
			city=cities[each_tweet];

			tweets[city].unshift([ 'User Names',"Number of Tweets"])
			
			chart_d=google.visualization.arrayToDataTable(tweets[city])
			var options = {
			  title: 'Top 10 users in '+city
			};
			var chart = new google.visualization.Histogram(document.getElementById('chart_id'+each_tweet));
			chart.draw(chart_d, options);
		}
	});



});

$("#retweet_user").click(function(){
$.get(server_url+"/user/fav",function(data){

		$("chart_id0").parent().html("<div id='chart_id0'></div>")

		tweets=data['data']
		console.log(tweets)
		tweets.unshift([ "Delhi","Mumbai"])
			
		chart_d=google.visualization.arrayToDataTable(tweets)
			var options = {
			  title: 'User retweet'+city
			};
			var chart = new google.visualization.Histogram(document.getElementById('chart_id0'));
			chart.draw(chart_d, options);
		
	});



});