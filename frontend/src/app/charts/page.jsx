"use client";
import { useEffect, useState } from "react";
import InfoSVG from "@/assets/svg/InfoSVG";
import { useRawData } from "@/components/RawDataContext";
import { useData } from "@/components/DataContext";
import axios from "@/lib/axios";
import { conTabs } from "@/lib/utils";
import StepsChart from "./StepsChart";

const Page = () => {
  const { rawData } = useRawData();
  const { data, setData } = useData();
  const [tabContingence, setTabContingence] = useState({});
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
  const [tabsConArr, setTabConArr] = useState([]);
  const [tables, setTables] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (rawData.file && data) {
          const formData = new FormData();
          formData.append("ordinal_cols", JSON.stringify(data));

          const tabDistanceResponse = await axios
            .post("create-distance-table/", formData, {
              headers: { "Content-Type": "multipart/form-data; charset=UTF-8" },
            })
            .catch((err) => console.error(err));
          const distanceTab = JSON.parse(tabDistanceResponse.data);
          setTabDistance(distanceTab);

          const tabBurtResponse = await axios
            .post("create-burt-table/", formData, {
              headers: { "Content-Type": "multipart/form-data; charset=UTF-8" },
            })
            .catch((err) => console.error(err));
          const BurtTab = JSON.parse(tabBurtResponse.data);
          setTabBurt(BurtTab);

          const tabContingenceResponse = await axios
            .post("create-contigence-table/", formData, {
              headers: { "Content-Type": "multipart/form-data; charset=UTF-8" },
            })
            .then((res) => {
              setTabContingence(res.data.tables);
            })
            .catch((err) => console.error(err));
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (!tabsConArr.length) {
      if (Object.keys(tabContingence).length > 0) {
        const res = conTabs(tabContingence);
        setTabConArr(res);

        const obj = {
          title: "Tableaux de contingences",
          content: { tabContingence: tabContingence, tabsConArr: res },
        };
        const obj1 = {
          title: "Tableau de Burt",
          content: tabBurt,
        };
        const obj2 = {
          title: "Tableau de Distance",
          content: tabDistance,
        };

        const obj3 = {
          title: "Colonnes ordinales",
        };

        setTables([obj, obj1, obj2, obj3]);
      }
    }
  }, [tabContingence]);

  return (
    <div className="flex flex-col h-fit w-full">
      {Object.keys(rawData.file).length == 0 ? (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see results in charts</p>{" "}
        </div>
      ) : (
        tables[0] && tables[1] && tables[2] && <StepsChart tables={tables} />
      )}
    </div>
  );
};

export default Page;
