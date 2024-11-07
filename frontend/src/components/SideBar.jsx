import React from "react";
import LogoSVG from "@/assets/svg/LogoSVG";
import { v4 as uuidv4 } from "uuid";
import HomeSVG from "@/assets/svg/HomeSVG";
import DataSVG from "@/assets/svg/DataSVG";
import TableSVG from "@/assets/svg/TableSVG";
import ChartsSVG from "@/assets/svg/ChartsSVG";
import CsvSVG from "@/assets/svg/CsvSVG";
import Link from "next/link";

const BarItems = [
  { id: uuidv4(), title: "Accueil", segment: "/", logo: <HomeSVG /> },
  {
    id: uuidv4(),
    title: "Data representation",
    segment: "/dataRepresentation",
    logo: <DataSVG />,
  },
  { id: uuidv4(), title: "Tables", segment: "/tables", logo: <TableSVG /> },
  { id: uuidv4(), title: "Charts", segment: "/charts", logo: <ChartsSVG /> },
  { id: uuidv4(), title: "Raw csv", segment: "/rawCsv", logo: <CsvSVG /> },
];

const SideBar = () => {
  return (
    <div className="flex flex-col w-[296px] h-full items-center justify-start">
      <div className="flex w-full h-fit items-center justify-between">
        <LogoSVG />
        <p>v1.0</p>
      </div>
      <div className="flex flex-col items-center justify-center gap-2.5 w-full h-fit">
        {BarItems.map((i) => (
          <Link
            href={i.segment}
            key={i.id}
            className="w-full h-10 flex items-center justify-start px-5 gap-5"
          >
            {i.logo}
            <p>{i.title}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default SideBar;
