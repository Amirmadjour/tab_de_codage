import { Button } from "@/components/ui/button";
import clsx from "clsx";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";
import Contingence from "./Contingence";
import HeatMap from "./HeatMap";
import VerticalBar from "./VerticalBar";

const StepsChart = ({ tables }) => {
  //Args Array of objects : {title: , content: }
  const [step, setStep] = useState(1);

  const increment = () => {
    setStep((prev) => prev + 1);
  };

  const decrement = () => {
    setStep((prev) => prev - 1);
  };

  return (
    <div className="w-full flex flex-col items-center justify-center gap-5">
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
      {step === 1 && <Contingence data={tables[0]} />}
      {step === 2 && <HeatMap content={tables[1].content} />}
      {step === 3 && <HeatMap content={tables[2].content} />}
      {step === 4 && <VerticalBar />}
    </div>
  );
};

export default StepsChart;
