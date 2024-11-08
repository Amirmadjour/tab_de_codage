import React, { useEffect, useState } from "react";
import Papa from "papaparse";
import VAROrdinale from "./VAROrdinale";
import ColumnOrder from "./ColumnOrder";
import axios from "axios";

const CSVUploader = ({ setFile, data, setData }) => {
  const [csvData, setCsvData] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);
  const [variablesOrdinales, setVariablesOrdinales] = useState([]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (file) {
      Papa.parse(file, {
        skipEmptyLines: true,
        complete: (results) => {
          setCsvData(results.data);
        },
        error: (error) => {
          console.error("Error while parsing CSV:", error);
        },
      });

      const formData = new FormData();
      formData.append("file", file);
      setFile(file);

      const res = await axios
        .post("http://127.0.0.1:8000/coding_table/api/csv-data/", formData)
        .catch((err) => console.error("Error while uploading csv file: ", err));
    }
  };

  useEffect(() => {
    function onlyUnique(value, index, array) {
      return array.indexOf(value) === index;
    }

    let variable_ordinales_valeurs_uniques = [];
    for (let col in variablesOrdinales.colonnes) {
      variable_ordinales_valeurs_uniques = [
        ...variable_ordinales_valeurs_uniques,
        csvData
          .slice(1)
          .map((i) => i[csvData[0].indexOf(variablesOrdinales.colonnes[col])])
          .filter(onlyUnique),
      ];
    }

    setColumnOrder(variable_ordinales_valeurs_uniques);
  }, [variablesOrdinales]);

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      <table>
        <thead>
          <tr>
            {csvData.length > 0 &&
              Object.keys(csvData[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>
        <tbody>
          {csvData.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {csvData.length != 0 && (
        <VAROrdinale
          colonnes={csvData[0]}
          setVariablesOrdinales={setVariablesOrdinales}
          setData={setData}
          data={data}
        />
      )}
      {columnOrder.length != 0 &&
        columnOrder.map((c, index) => (
          <ColumnOrder
            key={index}
            variables={c}
            reponses={variablesOrdinales}
            data={data}
            setData={setData}
            currentRep={variablesOrdinales.colonnes[index]}
          />
        ))}
    </div>
  );
};

export default CSVUploader;
