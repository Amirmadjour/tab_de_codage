import { useEffect, useState } from "react";
import DataHeatMap from "@/app/charts/DataHeatMap";

const ContingenceContainer = ({ content }) => {
  const [heatMapData, setHeatMapData] = useState();

  useEffect(() => {
    function formDataToHeatMap() {
      let arr = [];

      const vars = content.tableau.columns;
      const groups = content.tableau.index;
      const data = content.tableau.data;

      for (let i = 0; i < vars.length; i++) {
        for (let j = 0; j < groups.length; j++) {
          const obj = {
            group: groups[j],
            variable: vars[i],
            value: data[j][i],
          };
          arr = [...arr, obj];
        }
      }

      setHeatMapData(arr);
    }
    formDataToHeatMap();
  }, []);


  return (
    <div className="w-full h-full">
      {heatMapData && <DataHeatMap data={heatMapData} />}
    </div>
  );
};

export default ContingenceContainer;
