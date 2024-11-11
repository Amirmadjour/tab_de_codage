"use client";
import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import Papa from "papaparse";
import VAROrdinale from "./VAROrdinale";
import ColumnOrder from "./ColumnOrder";
import { useState, useEffect } from "react";
import axios from "axios";
import { useRawData } from "@/components/RawDataContext";
import FileUploadSVG from "@/assets/svg/FileUploadSVG";

export default function DropZone() {
  const { rawData, setRawData } = useRawData();


  const [columnOrder, setColumnOrder] = useState([]);
  const [variablesOrdinales, setVariablesOrdinales] = useState([]);

  const onDrop = useCallback(async (acceptedFiles) => {

    const file_acc = acceptedFiles[0];

    if (file_acc) {
      Papa.parse(file_acc, {
        skipEmptyLines: true,
        complete: (results) => {
          setRawData((prev) => ({ ...prev, csvData: results.data }));
        },
        error: (error) => {
          console.error("Error while parsing CSV:", error);
        },
      });

      const formData = new FormData();
      formData.append("file", file_acc);
      setRawData((prev) => ({ ...prev, file: file_acc }));

      const res = await axios
        .post("http://127.0.0.1:8000/coding_table/api/csv-data/", formData)
        .catch((err) => console.error("Error while uploading csv file: ", err));
    }
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  useEffect(() => {
    function onlyUnique(value, index, array) {
      return array.indexOf(value) === index;
    }

    let variable_ordinales_valeurs_uniques = [];
    for (let col in variablesOrdinales.colonnes) {
      variable_ordinales_valeurs_uniques = [
        ...variable_ordinales_valeurs_uniques,
        rawData.csvData
          .slice(1)
          .map(
            (i) =>
              i[rawData.csvData[0].indexOf(variablesOrdinales.colonnes[col])]
          )
          .filter(onlyUnique),
      ];
    }

    setColumnOrder(variable_ordinales_valeurs_uniques);
  }, [variablesOrdinales]);

  return (
    <div className="h-fit w-full flex flex-col items-center justify-center">
      <div
        {...getRootProps()}
        className="dashed w-full h-48 flex items-center justify-center my-2.5"
      >
        <input {...getInputProps()} accept=".csv, .xlsx" />
        {Object.keys(rawData.file).length > 0 ? (
          <p>{rawData.file.name}</p>
        ) : isDragActive ? (
          <p>Drop the files here</p>
        ) : (
          <div className="flex flex-col items-center justify-center gap-5">
            <FileUploadSVG />
            <div className="flex flex-col items-center justify-center gap-2.5">
              <p>Drag & Drop or Choose file to upload</p>
              <p className="text-foreground-secondary w-fit">csv</p>
            </div>
          </div>
        )}
      </div>
      {rawData.csvData.length != 0 && (
        <VAROrdinale
          colonnes={rawData.csvData[0]}
          setVariablesOrdinales={setVariablesOrdinales}
        />
      )}
      {columnOrder.length != 0 &&
        columnOrder.map((c, index) => (
          <ColumnOrder
            key={index}
            variables={c}
            reponses={variablesOrdinales}
            currentRep={variablesOrdinales.colonnes[index]}
          />
        ))}
    </div>
  );
}
