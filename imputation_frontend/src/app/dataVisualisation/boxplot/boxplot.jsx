import React, { useEffect, useRef } from "react";
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
  Colors,
  Tooltip,
} from "chart.js";
import {
  BoxPlotController,
  BoxAndWiskers,
} from "@sgratzl/chartjs-chart-boxplot";

Chart.register(
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
  BoxPlotController,
  BoxAndWiskers,
  Colors,
  Tooltip
);

export const MyChart = ({ boxplot_data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null); // Ref to store the Chart instance

  useEffect(() => {
    const ctx = chartRef.current;

    // Destroy the existing chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    console.log("boxplot_data.key: ", boxplot_data.key);
    console.log("boxplot_data.value: ", boxplot_data.value);

    const data = {
      labels: boxplot_data.key,
      datasets: boxplot_data.value,
    };

    chartInstance.current = new Chart(ctx, {
      type: "boxplot",
      data: data,
      options: {
        quantiles: "fivenum",
      },
    });

    // Cleanup: destroy the chart when the component unmounts
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, []);

  return (
    <div className="w-full h-full">
      <canvas ref={chartRef} id="myChart"></canvas>
    </div>
  );
};
