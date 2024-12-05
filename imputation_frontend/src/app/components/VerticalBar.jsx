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

const VerticalBar = ({ graphicData }) => {
  const generateGraphics = (graphicData) => {
    const data = {
      labels: Object.keys(graphicData),
      datasets: [
        {
          axis: "y",
          label: "Missing values",
          data: Object.values(graphicData),
          fill: false,
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
            <Bar className="w-full" data={data} options={{ indexAxis: "y" }} />
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

export default VerticalBar;
