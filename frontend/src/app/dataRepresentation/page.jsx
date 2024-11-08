"use client";
import { useState, useEffect } from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";
import { useRawData } from "@/components/RawDataContext";
import { useData } from "@/components/DataContext";
import axios from "axios";

ChartJS.register(Tooltip, Legend, ArcElement);

const page = () => {
  const [pieData, setPieData] = useState();
  const [error, setError] = useState();
  const { rawData } = useRawData();
  const { data } = useData();

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (Object.keys(rawData.file).length > 0) {
          console.log("It started fetching");

          const pieResponse = await axios
            .post("http://127.0.0.1:8000/coding_table/api/pie-data/", data)
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
        const PieData = {
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
        PieDataArr = [...PieDataArr, PieData];
      }
    }
    console.log("PieDataArr: ", PieDataArr);
    return (
      <div className="grid grid-cols-3">
        {data &&
          PieDataArr &&
          PieDataArr.map((p, index) => (
            <div key={index} className="w-full">
              <Pie data={p} />
            </div>
          ))}
      </div>
    );
  };

  console.log("pieData: ", pieData);

  return (
    <div>
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

export default page;
