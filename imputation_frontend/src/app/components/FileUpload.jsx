"use client";
import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload } from "lucide-react";
import Papa from "papaparse";
import { useState, useEffect } from "react";
import axios from "@/lib/axios";
import { useRawData } from "@/lib/RawDataContext";

export default function FileUpload({ setNotification }) {
  const { rawData, setRawData } = useRawData();

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
        .post("/csv-data/", formData)
        .then((res) => {
          if (res.status == 200) {
            setNotification();
          }
          console.log(res);
        })
        .catch((err) => console.error("Error while uploading csv file: ", err));
    }
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps()}
      className="w-full h-full flex items-center justify-center"
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the files here ...</p>
      ) : (
        <div className="flex flex-col items-center justify-center gap-2.5">
          <div className="w-fit h-fit p-[15px] rounded-full bg-background-secondary">
            <Upload className="text-foreground-secondary" />
          </div>
          <p>Upload a file</p>
        </div>
      )}
    </div>
  );
}
