"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import DropZone from "@/components/DropZone";
import CSVReader from "@/components/CSVReader";

ChartJS.register(Tooltip, Legend, ArcElement);

const App = () => {
  const [file, setFile] = useState();
  const [fileReady, setFileReady] = useState(false);

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
  const [pieData, setPieData] = useState();
  const [data, setData] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (file && fileReady && data) {
          console.log("It started fetching");

          const pieResponse = await axios
            .post("http://127.0.0.1:8000/coding_table/api/pie-data/", data)
            .catch((err) => console.error(err));
          setPieData(pieResponse.data);

          const response = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-coding-table/",
              data
            )
            .catch((err) => console.error(err));
          const codingTab = JSON.parse(response.data);
          setTabCodage(codingTab);

          const tabDisjonctifResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-coding-table-disjonctif-complet/",
              data
            )
            .catch((err) => console.error(err));
          const disjonctifTab = JSON.parse(tabDisjonctifResponse.data);
          setTabDisjonctif(disjonctifTab);

          const tabDistanceResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-distance-table/",
              data
            )
            .catch((err) => console.error(err));
          const distanceTab = JSON.parse(tabDistanceResponse.data);
          console.log("DistanceTab: ", distanceTab);
          setTabDistance(distanceTab);

          const tabBurtResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-burt-table/",
              data
            )
            .catch((err) => console.error(err));
          const BurtTab = JSON.parse(tabBurtResponse.data);
          setTabBurt(BurtTab);
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, [fileReady]);

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

  return (
    <div className="flex w-full h-full items-center justify-center gap-2.5 p-2.5">
      {error && <p style={{ color: "red" }}>{error}</p>}

      <CSVReader setFile={setFile} data={data} setData={setData} />

      {file && (
        <Button
          onClick={async () => {
            setFileReady((val) => !val);
          }}
        >
          Traiter le fichier
        </Button>
      )}

      {pieData && (
        <>
          <h2 className="text-gray-700 text-3xl font-bold text-left w-full">
            Representation des données
          </h2>
          {generateGraphics(pieData)}
        </>
      )}

      {tabCodage.data.length != 0 && (
        <>
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
        </>
      )}
      {tabDisjonctif.data.length != 0 && (
        <>
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
        </>
      )}

      {tabDistance.data.length != 0 && (
        <>
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
        </>
      )}

      {tabBurt.data.length != 0 && (
        <>
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
        </>
      )}
    </div>
  );
};

export default App;
