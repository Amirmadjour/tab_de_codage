import { useEffect, useState } from "react";
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
  Tooltip,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// Register the components
Chart.register(CategoryScale, LinearScale, BarController, BarElement, Tooltip);

const StackedBar = ({ content }) => {
  const generateGraphics = (graphData) => {
    let stackedBarData;

    const datasets = graphData.data.map((dataArray, i) => ({
      label: graphData.index[i], // Label for the dataset
      data: dataArray, // Data array for this dataset
      fill: false,
      backgroundColor: [
        "rgba(255, 99, 132, 0.2)",
        "rgba(255, 159, 64, 0.2)",
        "rgba(255, 205, 86, 0.2)",
        "rgba(75, 192, 192, 0.2)",
        "rgba(54, 162, 235, 0.2)",
        "rgba(153, 102, 255, 0.2)",
        "rgba(201, 203, 207, 0.2)",
      ][i % 7],
      borderColor: [
        "rgb(255, 99, 132)",
        "rgb(255, 159, 64)",
        "rgb(255, 205, 86)",
        "rgb(75, 192, 192)",
        "rgb(54, 162, 235)",
        "rgb(153, 102, 255)",
        "rgb(201, 203, 207)",
      ][i % 7],
      borderWidth: 1,
      hoverOffset: 4,
    }));

    stackedBarData = {
      labels: graphData.columns,
      datasets,
    };

    return (
      <div className="w-full flex flex-col ">
        {stackedBarData && (
          <div className="w-full">
            <Bar
              className="w-full"
              data={stackedBarData}
              options={{
                indexAxis: "y",
                scales: { y: { stacked: true }, x: { stacked: true } },
              }}
            />
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="w-full flex items-center justify-center">
      {content && generateGraphics(content)}
    </div>
  );
};

export default StackedBar;
