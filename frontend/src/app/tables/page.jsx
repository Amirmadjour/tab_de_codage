"use client";
import { useRawData } from "@/components/RawDataContext";
import { useState, useEffect } from "react";
import InfoSVG from "@/assets/svg/InfoSVG";
import { useData } from "@/components/DataContext";
import axios from "axios";
import Tables from "./Tables";
import { v4 as uuidv4 } from "uuid";

const page = () => {
  const { rawData } = useRawData();
  const { data, setData } = useData();
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
  const [tabContingence, setTabContingence] = useState({});
  const [tables, setTables] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (rawData.file && data) {
          const response = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-coding-table/",
              data
            )
            .catch((err) => console.error(err));
          const codingTab = JSON.parse(response.data);
          setTabCodage(codingTab);
          const obj1 = {
            id: uuidv4(),
            title: "Tableau de codage",
            content: codingTab,
          };

          const tabDisjonctifResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-coding-table-disjonctif-complet/",
              data
            )
            .catch((err) => console.error(err));
          const disjonctifTab = JSON.parse(tabDisjonctifResponse.data);
          setTabDisjonctif(disjonctifTab);
          const obj2 = {
            id: uuidv4(),
            title: "Tableau de codage disjonctif",
            content: disjonctifTab,
          };

          const tabDistanceResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-distance-table/",
              data
            )
            .catch((err) => console.error(err));
          const distanceTab = JSON.parse(tabDistanceResponse.data);
          setTabDistance(distanceTab);
          const obj3 = {
            id: uuidv4(),
            title: "Tableau de Distance",
            content: distanceTab,
          };

          const tabBurtResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-burt-table/",
              data
            )
            .catch((err) => console.error(err));
          const BurtTab = JSON.parse(tabBurtResponse.data);
          setTabBurt(BurtTab);
          const obj4 = {
            id: uuidv4(),
            title: "Tableau de Burt",
            content: BurtTab,
          };

          let obj5 = {};
          const tabContingenceResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-contigence-table/",
              data
            )
            .then((res) => {
              setTabContingence(res.data.tables);
              obj5 = {
                id: uuidv4(),
                title: "Tableaux de contingences",
                content: res.data.tables,
              };
            })
            .catch((err) => console.error(err));

          setTables([obj1, obj2, obj3, obj4, obj5]);

          console.log([obj1, obj2, obj3, obj4, obj5]);
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="flex flex-col h-fit w-full gap-5">
      {Object.keys(rawData.file).length == 0 ? (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see results in tables</p>{" "}
        </div>
      ) : (
        tables[4] && <Tables tables={tables} />
      )}
    </div>
  );
};

export default page;
