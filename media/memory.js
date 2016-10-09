var memory_ns = {};
memory_ns.vis = d3.select('#memory_visualisation'),
    WIDTH = 1000, HEIGHT = 500, MARGINS = { top: 20,
                                            right: 20,
                                            bottom: 20,
                                            left: 50 },

    memory_ns.xScale = d3.scaleLinear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([250000,3700000]),            
    memory_ns.yScale = d3.scaleLinear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,320]),
    memory_ns.xAxis = d3.axisBottom()
			.scale(memory_ns.xScale),

    memory_ns.yAxis = d3.axisLeft()
			.scale(memory_ns.yScale);

memory_ns.vis.append("svg:g")
	 .attr("class", "axis")
	 .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
	 .call(memory_ns.xAxis);

memory_ns.vis.append("svg:g")
	 .attr("class", "axis")
	 .attr("transform", "translate(" + (MARGINS.left) + ",0)")
	 .call(memory_ns.yAxis);

memory_ns.lineGen = d3.line()
		      .x(function(d) {
			  return memory_ns.xScale(+d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1"));
		      })
		      .y(function(d) {
			  return memory_ns.yScale(+d.MemoryAvg);
		      });


d3.csv("data/test_simple.csv", function(error, data) {
    var lastelem = data.length - 1;
    
    memory_ns.vis.append('svg:path')
             .attr('d', memory_ns.lineGen(data))
             .attr('stroke', 'green')
             .attr('stroke-width', 2)
             .attr('fill', 'none');
    
    memory_ns.vis.selectAll(".point")
	     .data(data)
	     .enter().append("circle")
	     .attr("r", 4)
	     .attr("cx", function(d) { return memory_ns.xScale(d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	     .attr("cy", function(d) { return memory_ns.yScale(d.MemoryAvg); });

    memory_ns.vis.selectAll(".label")
	     .data([data[data.length-1]])
	     .enter().append("text")
	     .attr("x", function(d) {
		 var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 80000;
		 return memory_ns.xScale(xPosition);
	     })
	     .attr("y", function(d) {
		 var yPosition = +d.MemoryAvg + 6;
		 return memory_ns.yScale(yPosition);
	     })
	     .text("SIMPLE");
    
});

d3.csv("data/test_sqfile.csv", function(error, data) {
    memory_ns.vis.append('svg:path')
             .attr('d', memory_ns.lineGen(data))
             .attr('stroke', 'red')
             .attr('stroke-width', 2)
             .attr('fill', 'none');
    
    memory_ns.vis.selectAll(".point")
	     .data(data)
	     .enter().append("circle")
	     .attr("r", 4)
	     .attr("cx", function(d) { return memory_ns.xScale(d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	     .attr("cy", function(d) { return memory_ns.yScale(d.MemoryAvg); });

    memory_ns.vis.selectAll(".label")
	       .data([data[data.length-1]])
	       .enter().append("text")
	       .attr("x", function(d) {
		   var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 140000;
		   return memory_ns.xScale(xPosition);
	       })
	       .attr("y", function(d) {
		   var yPosition = +d.MemoryAvg + 5;
		   return memory_ns.yScale(yPosition);
	       })
	       .text("SQLITE FILE");


});

d3.csv("data/test_sqmemory.csv", function(error, data) {
    memory_ns.vis.append('svg:path')
             .attr('d', memory_ns.lineGen(data))
             .attr('stroke', 'blue')
             .attr('stroke-width', 2)
             .attr('fill', 'none');

    memory_ns.vis.selectAll(".point")
	     .data(data)
	     .enter().append("circle")
	     .attr("r", 4)
	     .attr("cx", function(d) { return memory_ns.xScale(d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1")); })
	     .attr("cy", function(d) { return memory_ns.yScale(d.MemoryAvg); });

    memory_ns.vis.selectAll(".label")
	     .data([data[data.length-1]])
	     .enter().append("text")
	     .attr("x", function(d) {
		 var xPosition = +d.fileName.replace(/demo_\d+_([0-9]+).csv/i, "$1") - 160000;
		 return memory_ns.
				 xScale(xPosition);
	     })
	     .attr("y", function(d) {
		 var yPosition = +d.MemoryAvg + 4;
		 return memory_ns.yScale(yPosition);
	     })
	     .text("SQLITE MEMORY");
    
});
