"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

ChartJS.register(Tooltip, Legend, ArcElement);

const App = () => {
  const [tabCodage, setTabCodage] = useState({
    columns: [],
    index: [],
    data: [],
  });
  const [tabDisjonctif, setTabDisjonctif] = useState({
    columns: [],
    index: [],
    data: [],
  });
  const [tabDistance, setTabDistance] = useState({
    columns: [],
    index: [],
    data: [],
  });
  const [tabBurt, setTabBurt] = useState({
    columns: [],
    index: [],
    data: [],
  });
  const [data, setData] = useState();
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/create-coding-table/"
        );
        const codingTab = JSON.parse(response.data);
        setTabCodage(codingTab);

        const tabDisjonctifResponse = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/create-coding-table-disjonctif-complet/"
        );
        const disjonctifTab = JSON.parse(tabDisjonctifResponse.data);
        setTabDisjonctif(disjonctifTab);

        const tabDistanceResponse = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/create-distance-table/"
        );
        const distanceTab = JSON.parse(tabDistanceResponse.data);
        console.log("DistanceTab: ", distanceTab);
        setTabDistance(distanceTab);

        const tabBurtResponse = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/create-burt-table/"
        );
        const BurtTab = JSON.parse(tabBurtResponse.data);
        setTabBurt(BurtTab);

        const pieResponse = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/pie-data/"
        );
        setData(pieResponse.data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  console.log("Pie data:", data);

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
                "rgba(153, 99, 35, 0.6)",
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
          PieDataArr.map((p) => (
            <div className="w-full">
              <Pie data={p} />
            </div>
          ))}
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center justify-center gap-5 py-5 w-2/3">
      {error && <p style={{ color: "red" }}>{error}</p>}
      {generateGraphics(data)}
      <h2 className="text-gray-700 text-3xl font-bold text-left w-full">
        Tableau de codage
      </h2>
      <Table className="">
        <TableHeader>
          <TableRow>
            {tabCodage.columns.map((i, index) => (
              <TableHead key={index}>V{index}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {tabCodage.data.map((i, i_index) => (
            <TableRow key={i_index}>
              {i.map((j, j_index) => (
                <TableCell key={i_index.toString() + j_index.toString()}>
                  {j}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <h2 className="text-gray-700 text-3xl font-bold text-left w-full">
        Tableau de codage disjonctif complet
      </h2>
      <Table className="">
        <TableHeader>
          <TableRow>
            {tabDisjonctif.columns.map((i, index) => (
              <TableHead key={index}>{i}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {tabDisjonctif.data.map((i, i_index) => (
            <TableRow key={i_index}>
              {i.map((j, j_index) => (
                <TableCell key={i_index.toString() + j_index.toString()}>
                  {j}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <h2 className="text-gray-700 text-3xl font-bold text-left w-full">
        Tableau de Distance
      </h2>
      <Table className="">
        <TableHeader>
          <TableRow>
            {tabDistance.columns.map((i, index) => (
              <TableHead key={index}>{i}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {tabDistance.data.map((i, i_index) => (
            <TableRow key={i_index}>
              {i.map((j, j_index) => (
                <TableCell key={i_index.toString() + j_index.toString()}>
                  {j}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <h2 className="text-gray-700 text-3xl font-bold text-left w-full">
        Tableau de Burt
      </h2>
      <Table className="">
        <TableHeader>
          <TableRow>
            {tabBurt.columns.map((i, index) => (
              <TableHead key={index}>{i}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {tabBurt.data.map((i, i_index) => (
            <TableRow key={i_index}>
              {i.map((j, j_index) => (
                <TableCell key={i_index.toString() + j_index.toString()}>
                  {j}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default App;
