import React, { useEffect, useState } from "react";
import SingleTable from "./SingleTable";
import { v4 as uuidv4 } from "uuid";
import ContingenceTable from "./ContingenceTable";
import { conTabs } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight } from "lucide-react";
import clsx from "clsx";

const Tables = ({ tables }) => {
  const [tabsConArr, setTabConArr] = useState([]);
  const [step, setStep] = useState(1);

  const increment = () => {
    setStep((prev) => prev + 1);
  };

  const decrement = () => {
    setStep((prev) => prev - 1);
  };

  const items = tables.slice(0, 4);

  const tabContingence = tables[4].content;

  //Tabs de contingences
  useEffect(() => {
    if (Object.keys(tabContingence).length > 0) {
      setTabConArr(conTabs(tabContingence));
    }
  }, [tabContingence]);

  return (
    <div className="flex flex-col items-center justify-center gap-10">
      <div className="w-full flex items-center justify-between">
        <Button
          onClick={decrement}
          className={clsx(
            "rounded-full bg-hover w-10 h-10 p-0",
            step === 1 && "opacity-0 -z-10"
          )}
        >
          <ChevronLeft className="text-popover-foreground" />
        </Button>
        <h2 className="text-3xl font-bold text-left">
          {tables[step - 1].title}
        </h2>
        <Button
          onClick={increment}
          className={clsx(
            "rounded-full bg-hover w-10 h-10 p-0",
            step === tables.length && "opacity-0 -z-10"
          )}
        >
          <ChevronRight className="text-popover-foreground" />
        </Button>
      </div>
      {items.map(
        (i, index) =>
          step === index + 1 && (
            <SingleTable key={i.id} title={i.title} content={i.content} />
          )
      )}
      {Object.keys(tabContingence).length > 0 &&
        step === 5 &&
        tabsConArr.map((i, index) => (
          <ContingenceTable key={index} content={i} />
        ))}
    </div>
  );
};

export default Tables;
