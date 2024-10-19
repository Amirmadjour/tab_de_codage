"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/data/")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h1>Data from Django:</h1>
      {data ? <p>{data.message}</p> : <p>Loading...</p>}
    </div>
  );
}
