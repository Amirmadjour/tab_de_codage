"use client";
import { useEffect, useState } from "react";
import InfoSVG from "@/assets/svg/InfoSVG";
import { useRawData } from "@/components/RawDataContext";
import { useData } from "@/components/DataContext";
import axios from "axios";
import { conTabs } from "@/lib/utils";
import ContingenceContainer from "@/app/charts/ContingenceContainer";

const page = () => {
  const { rawData } = useRawData();
  const { data, setData } = useData();
  const [tabContingence, setTabContingence] = useState({});
  const [tabsConArr, setTabConArr] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (rawData.file && data) {
          const tabContingenceResponse = await axios
            .post(
              "http://127.0.0.1:8000/coding_table/api/create-contigence-table/",
              data
            )
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
      console.log("tabContingence: ", tabContingence);
      if (Object.keys(tabContingence).length > 0) {
        setTabConArr(conTabs(tabContingence));
      }
    }
  }, [tabContingence]);

  console.log("Times: ", tabsConArr);

  return (
    <div className="flex flex-col h-fit w-full">
      {Object.keys(rawData.file).length == 0 && (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see results in charts</p>{" "}
        </div>
      )}
      {Object.keys(tabContingence).length > 0 &&
        tabsConArr.map((i, index) => (
          <ContingenceContainer key={index} content={i} />
        ))}
    </div>
  );
};

export default page;
