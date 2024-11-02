import React, { useEffect, useState } from "react";
import Papa from "papaparse";
import VAROrdinale from "./VAROrdinale";
import ColumnOrder from "./ColumnOrder";

const CSVUploader = () => {
  const [data, setData] = useState([]);
  const [variablesOrdinales, setVariablesOrdinales] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      Papa.parse(file, {
        skipEmptyLines: true,
        complete: (results) => {
          setData(results.data);
          console.log(results.data);
        },
        error: (error) => {
          console.error("Error while parsing CSV:", error);
        },
      });
    }
  };

  useEffect(() => {
    function onlyUnique(value, index, array) {
      return array.indexOf(value) === index;
    }

    setColumnOrder(
      data
        .slice(1)
        .map((i) => i[data[0].indexOf(variablesOrdinales.colonnes[0])])
        .filter(onlyUnique)
    );
  }, [variablesOrdinales]);

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      <table>
        <thead>
          <tr>
            {data.length > 0 &&
              Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {data.length != 0 && (
        <VAROrdinale
          colonnes={data[0]}
          setVariablesOrdinales={setVariablesOrdinales}
        />
      )}
      {columnOrder.length != 0 && <ColumnOrder variables={columnOrder} />}
    </div>
  );
};

export default CSVUploader;
