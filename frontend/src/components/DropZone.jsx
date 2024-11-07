import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useState } from "react";

export default function DropZone() {
  const [csvFile, setCsvFile] = useState([]);
  const onDrop = useCallback((acceptedFiles) => {
    console.log(acceptedFiles);
    setCsvFile(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} className="dashed w-full h-48">
      <input {...getInputProps()} />
      {csvFile[0] ? (
        <p>{csvFile[0].name}</p>
      ) : isDragActive ? (
        <p>Drop the files here</p>
      ) : (
        <p>Drag {'n'} drop some files here, or click to select files</p>
      )}
    </div>
  );
}
