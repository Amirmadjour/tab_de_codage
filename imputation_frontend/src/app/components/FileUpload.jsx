"use client";
import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload } from "lucide-react";

export default function FileUpload() {
  const onDrop = useCallback((acceptedFiles) => {
    // Do something with the files
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
            <Upload className="text-foreground-secondary"/>
          </div>
          <p>Upload a file</p>
        </div>
      )}
    </div>
  );
}
