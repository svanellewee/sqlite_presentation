var duration_ns = {};
duration_ns.vis = d3.select('#duration_visualisation'),
    WIDTH = 1000, HEIGHT = 500, MARGINS = { top: 20,
                                            right: 20,
                                            bottom: 20,
                                            left: 50 },

    duration_ns.xScale = d3.scaleLinear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([250000,3700000]),            
    duration_ns.yScale = d3.scaleLinear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,90]),
    duration_ns.xAxis = d3.axisBottom()
			  .scale(duration_ns.xScale),

    duration_ns.yAxis = d3.axisLeft()
			  .scale(duration_ns.yScale);

duration_ns.vis.append("svg:g")
	   .attr("class", "axis")
	   .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
	   .call(duration_ns.xAxis);

duration_ns.vis.append("svg:g")
	   .attr("class", "axis")
	   .attr("transform", "translate(" + (MARGINS.left) + ",0)")
	   .call(duration_ns.yAxis);

duration_ns.lineGen = d3.line()
			.x(function(d) {
			    return duration_ns.xScale(+d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1"));
			})
			.y(function(d) {
			    return duration_ns.yScale(+d.duration);
			});


d3.csv("data/test_simple.csv", function(error, data) {
    duration_ns.vis.append('svg:path')
               .attr('d', duration_ns.lineGen(data))
               .attr('stroke', 'green')
               .attr('stroke-width', 4)
               .attr('fill', 'none');

    duration_ns.vis.selectAll(".point")
	       .data(data)
	       .enter().append("circle")
	       .attr("r", 4)
	       .attr("cx", function(d) { return duration_ns.xScale(+d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	       .attr("cy", function(d) { return duration_ns.yScale(+d.duration); });

    duration_ns.vis.selectAll(".label")
	       .data([data[data.length-1]])
	       .enter().append("text")
	       .attr("x", function(d) {
		   var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 90000;
		   return duration_ns.xScale(xPosition);
	       })
	       .attr("y", function(d) {
		   var yPosition = +d.duration + 1;
		   return duration_ns.yScale(yPosition); ; })
	       .text("SIMPLE");
});

d3.csv("data/test_sqfile.csv", function(error, data) {
    duration_ns.vis.append('svg:path')
               .attr('d', duration_ns.lineGen(data))
               .attr('stroke', 'red')
               .attr('stroke-width', 2)
               .attr('fill', 'none');

    duration_ns.vis.selectAll(".point")
	       .data(data)
	       .enter().append("circle")
	       .attr("r", 4)
	       .attr("cx", function(d) { return duration_ns.xScale(+d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	       .attr("cy", function(d) { return duration_ns.yScale(+d.duration); });
    
    duration_ns.vis.selectAll(".label")
	       .data([data[data.length-1]])
	       .enter().append("text")
	       .attr("x", function(d) {
		   var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 100000;
		   return duration_ns.xScale(xPosition);
	       })
	       .attr("y", function(d) {
		   var yPosition = +d.duration - 4;
		   return duration_ns.yScale(yPosition);
	       })
	       .text("SQLITE FILE");

});

d3.csv("data/test_sqmemory.csv", function(error, data) {
    duration_ns.vis.append('svg:path')
               .attr('d', duration_ns.lineGen(data))
               .attr('stroke', 'blue')
               .attr('stroke-width', 2)
               .attr('fill', 'none');

    duration_ns.vis.selectAll(".point")
	       .data(data)
	       .enter().append("circle")
	       .attr("r", 4)
	       .attr("cx", function(d) { return duration_ns.xScale(+d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	       .attr("cy", function(d) { return duration_ns.yScale(+d.duration); });

    duration_ns.vis.selectAll(".label")
	       .data([data[data.length-1]])
	       .enter().append("text")
	       .attr("x", function(d) {
		   var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 150000;
		   return duration_ns.xScale(xPosition);
	       })
	       .attr("y", function(d) {
		   var yPosition = +d.duration + 1;
		   return duration_ns.yScale(yPosition);
	       })
	       .text("SQLITE MEMORY");    
});
