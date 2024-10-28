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
  //Not real columns, only the size
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [sexe, setSexe] = useState([]);

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
        

        const second_res = await axios.get(
          "http://127.0.0.1:8000/coding_table/api/csv-data/"
        );
        const csv_data = JSON.parse(second_res.data);
        setData(csv_data);

        const column = csv_data.map((row) => row[0]);
        setSexe(column);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  const SexePieData = {
    labels: ["Feminin", "Masculin"],
    datasets: [
      {
        label: "Sexe",
        data: [15, 85],
        backgroundColor: ["rgba(255, 99, 132, 0.6", "rgba(54, 162, 235, 0.6)"],
        hoverOffset: 4,
      },
    ],
  };

  return (
    <div className="flex flex-col items-center justify-center gap-5 py-5 w-2/3">
      {error && <p style={{ color: "red" }}>{error}</p>}
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

      <ul>
        {data.map((i, index) => (
          <li key={index}>{i}</li>
        ))}
      </ul>
      <div className="w-1/2">
        <Pie data={SexePieData} />
      </div>
    </div>
  );
};

export default App;
