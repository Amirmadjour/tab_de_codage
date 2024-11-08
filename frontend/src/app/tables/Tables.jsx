import React, { useEffect, useState } from "react";
import SingleTable from "./SingleTable";
import { v4 as uuidv4 } from "uuid";
import ContingenceTable from "./ContingenceTable";
import { conTabs } from "@/lib/utils";

const Tables = ({
  tabBurt,
  tabCodage,
  tabDisjonctif,
  tabDistance,
  tabContingence,
}) => {
  const [tabsConArr, setTabConArr] = useState([]);

  const items = [
    { id: uuidv4(), title: "Tableau de codage", content: tabCodage },
    {
      id: uuidv4(),
      title: "Tableau de codage disjonctif complet",
      content: tabDisjonctif,
    },
    { id: uuidv4(), title: "Tableau de Distance", content: tabDistance },
    { id: uuidv4(), title: "Tableau de Burt", content: tabBurt },
  ];

  //Tabs de contingences
  useEffect(() => {
    if (Object.keys(tabContingence).length > 0) {
      setTabConArr(conTabs(tabContingence));
    }
  }, [tabContingence]);

  return (
    <div className="flex flex-col items-center justify-center gap-5">
      {items.map((i) => (
        <SingleTable key={i.id} title={i.title} content={i.content} />
      ))}
      <h2 className="text-3xl font-bold text-left w-full">
        Tableaux de contingences
      </h2>
      {Object.keys(tabContingence).length > 0 &&
        tabsConArr.map((i) => <ContingenceTable content={i} />)}
    </div>
  );
};

export default Tables;
