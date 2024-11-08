import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

const DataHeatMap = ({ data }) => {
  const svgRef = useRef(null);
  useEffect(() => {
    d3.select(svgRef.current).selectAll("*").remove();

    // Set dimensions and margins for the heatmap
    const margin = { top: 80, right: 25, bottom: 30, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3
      .select(svgRef.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Extract unique groups and variables
    const myGroups = Array.from(new Set(data.map((d) => d.group)));
    const myVars = Array.from(new Set(data.map((d) => d.variable)));

    // Build X scales and axis:
    var x = d3.scaleBand().range([0, width]).domain(myGroups).padding(0.05);
    svg
      .append("g")
      .style("font-size", 15)
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickSize(0))
      .select(".domain")
      .remove();

    // Build Y scales and axis:
    var y = d3.scaleBand().range([height, 0]).domain(myVars).padding(0.05);
    svg
      .append("g")
      .style("font-size", 15)
      .call(d3.axisLeft(y).tickSize(0))
      .select(".domain")
      .remove();

    const maxValue = Math.max(...data.map((obj) => obj.value));
    // Build color scale
    var myColor = d3
      .scaleLinear()
      .domain([0, maxValue])
      .range(["#f7fbff", "#32D5F1"]);

    // create a tooltip
    const Tooltip = d3
      .select("#something")
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("color", "white")
      .style("font-size", "12px")
      .style("background-color", "#151515E6")
      .style("border-radius", "5px")
      .style("padding", "5px");

    // Three function that change the tooltip when user hover / move / leave a cell
    const mouseover = (event, d) => {
      Tooltip.style("opacity", 1);
      d3.select(event.currentTarget)
        .style("stroke", "#1C274C")
        .style("opacity", 1);
    };

    const mousemove = function (event, d) {
      Tooltip.html("The exact value of<br>this cell is: " + d.value)
        .style("left", event.pageX + 10 + "px") // Tooltip follows mouse
        .style("top", event.pageY + 10 + "px"); // Tooltip follows mouse
    };

    const mouseleave = (event, d) => {
      Tooltip.style("opacity", 0);
      d3.select(event.currentTarget)
        .style("stroke", "none")
        .style("opacity", 0.8);
    };

    // add the squares
    svg
      .selectAll()
      .data(data, function (d) {
        return d.group + ":" + d.variable;
      })
      .enter()
      .append("rect")
      .attr("x", function (d) {
        return x(d.group);
      })
      .attr("y", function (d) {
        return y(d.variable);
      })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth())
      .attr("height", y.bandwidth())
      .style("fill", function (d) {
        return myColor(d.value);
      })
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave);
  }, []);

  return <div className="w-full h-full" ref={svgRef} id="something"></div>;
};

export default DataHeatMap;
