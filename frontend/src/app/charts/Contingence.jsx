import HeatMap from "./HeatMap";

const Contingence = ({ data }) => {
  return (
    <div className="w-full flex flex-col items-center justify-center">
      {Object.keys(data.content.tabContingence).length > 0 && (
        <div className="w-full flex flex-col items-center justify-center">
          {data.content.tabsConArr.map((i, index) => (
            <HeatMap key={index} content={i.tableau} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Contingence;
