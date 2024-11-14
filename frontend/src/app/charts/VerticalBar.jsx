import { useEffect, useState } from "react";
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
  Tooltip,
} from "chart.js";
import { useData } from "@/components/DataContext";
import { Bar } from "react-chartjs-2";
import axios from "@/lib/axios";
import { useRawData } from "@/components/RawDataContext";

// Register the components
Chart.register(CategoryScale, LinearScale, BarController, BarElement, Tooltip);

const VerticalBar = () => {
  const [pieData, setPieData] = useState();
  const [error, setError] = useState();
  const { rawData, setRawData } = useRawData();
  const { data, setData } = useData();

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (Object.keys(rawData.file).length > 0) {
          const pieResponse = await axios
            .post("pie-data/", data)
            .then((res) => setPieData(res.data))
            .catch((err) => console.error(err));
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  const generateGraphics = (graphData) => {
    let PieDataArr = [];
    if (graphData) {
      for (const key in data) {
        console.log("key: ", key);
        console.log("data: ", data);
        const PieData = {
          labels: Object.keys(graphData[key]),
          datasets: [
            {
              axis: "y",
              label: "Ordinal columns",
              data: Object.values(graphData[key]),
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
        PieDataArr = [...PieDataArr, PieData];
      }
    }
    return (
      <div className="w-full flex flex-col ">
        {data &&
          PieDataArr &&
          PieDataArr.map((p, index) => (
            <div key={index} className="w-full">
              <Bar className="w-full" data={p} options={{ indexAxis: "y" }} />
            </div>
          ))}
      </div>
    );
  };

  if (error) return <div className="text-destructive">{error}</div>;

  // Ensure the canvas has a defined height
  return (
    <div className="w-full flex items-center justify-center">
      {pieData && generateGraphics(pieData)}
    </div>
  );
};

export default VerticalBar;
