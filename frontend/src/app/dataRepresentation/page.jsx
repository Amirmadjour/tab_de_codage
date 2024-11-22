"use client";
import { useState, useEffect } from "react";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
} from "chart.js";
import { useRawData } from "@/components/RawDataContext";
import { useData } from "@/components/DataContext";
import axios from "@/lib/axios";
import InfoSVG from "@/assets/svg/InfoSVG";

ChartJS.register(
  CategoryScale,
  Legend,
  ArcElement,
  LinearScale,
  BarController,
  BarElement,
  Tooltip
);

const Page = () => {
  const [pieData, setPieData] = useState();
  const [error, setError] = useState();
  const { rawData } = useRawData();
  const { data } = useData();

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

  const generateGraphics = (data) => {
    let PieDataArr = [];
    if (data) {
      for (const key in data) {
        console.log("Number: ", key);
        const baseDataset = {
          labels: Object.keys(data[key]),
          datasets: [
            {
              label: "Number",
              data: Object.values(data[key]),
              backgroundColor: [
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 99, 132, 0.6)",
                "rgba(255, 206, 86, 0.6)",
                "rgba(75, 192, 192, 0.6)",
                "rgba(153, 102, 255, 0.6)",
                "rgba(153, 192, 35, 0.6)",
              ],
              hoverOffset: 4,
            },
          ],
        };

        const pieDataCopy = JSON.parse(JSON.stringify(baseDataset));
        const barDataCopy = JSON.parse(JSON.stringify(baseDataset));

        PieDataArr = [...PieDataArr, { pie: barDataCopy, bar: pieDataCopy }];
      }
    }
    console.log("PieDataArr: ", PieDataArr);
    return (
      <div className="grid grid-cols-3">
        {data &&
          PieDataArr &&
          PieDataArr.map((p, index) => (
            <div key={index} className="w-full">
              <Pie data={p.bar} />
              <Bar data={p.pie} />
            </div>
          ))}
      </div>
    );
  };

  return (
    <div className="w-full">
      {Object.keys(rawData.file).length == 0 && (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see data using pie charts</p>{" "}
        </div>
      )}
      {pieData && (
        <>
          <h2 className="text-3xl font-bold text-left w-full">
            Representation des données
          </h2>
          {generateGraphics(pieData)}
        </>
      )}
    </div>
  );
};

export default Page;
