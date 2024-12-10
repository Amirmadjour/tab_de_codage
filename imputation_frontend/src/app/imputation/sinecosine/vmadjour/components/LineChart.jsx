/*"use client";
import {
  Chart,
  CategoryScale,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

// Register the components
Chart.register(
  CategoryScale,
  LinearScale,
  LineElement,
  LineController,
  PointElement,
  Tooltip
);

const LineChart = ({ graphicData }) => {
  const generateGraphics = (graphicData) => {
    const data = {
      labels: Object.keys(graphicData),
      datasets: [
        {
          label: "Missing values",
          data: Object.values(graphicData),
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 205, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(201, 203, 207, 0.2)",
          ],
          borderColor: [
            "rgb(255, 99, 132)",
            "rgb(255, 159, 64)",
            "rgb(255, 205, 86)",
            "rgb(75, 192, 192)",
            "rgb(54, 162, 235)",
            "rgb(153, 102, 255)",
            "rgb(201, 203, 207)",
          ],
          borderWidth: 1,
          hoverOffset: 4,
        },
      ],
    };

    return (
      <div className="w-full flex flex-col ">
        {data && (
          <div className="w-full">
            <Line className="w-full" data={data} />
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="w-full flex items-center justify-center">
      {generateGraphics(graphicData)}
    </div>
  );
};

export default LineChart;*/

"use client";
import {
  Chart,
  CategoryScale,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { useState, useEffect } from "react";

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  LineElement,
  LineController,
  PointElement,
  Tooltip
);

const LineChart = ({ chartData }) => {
  /*const [dataPoints, setDataPoints] = useState([]);
  const [labels, setLabels] = useState([]);
  const [counter, setCounter] = useState(0); 

  useEffect(() => {
    const interval = setInterval(() => {
      const newDataPoint = Math.floor(Math.random() * 100); // Random data for demo

      setDataPoints((prevData) => {
        const newData = [...prevData, newDataPoint];
        return newData;
      });

      setLabels((prevLabels) => {
        const newLabel = `Sec ${counter}`;
        const newLabels = [...prevLabels, newLabel];
        return newLabels;
      });

      setCounter((prevCounter) => prevCounter + 1);
    }, 1000); 

    return () => clearInterval(interval); 
  }, [counter]);*/

  const data = {
    labels: chartData ? Object.keys(chartData) : [],
    datasets: [
      {
        label: "Real-time Data",
        data: chartData ? Object.values(chartData) : [],
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgb(75, 192, 192)",
        borderWidth: 1,
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="w-full grow flex items-center justify-center">
      <Line
        data={data}
        options={{
          responsive: true,
          maintainAspectRatio: false,
        }}
      />
    </div>
  );
};

export default LineChart;
