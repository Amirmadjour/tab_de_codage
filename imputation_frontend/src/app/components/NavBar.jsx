"use client";

import { v4 as uuidv4 } from "uuid";
import NavBtn from "./NavBtn";
import { Button } from "@/components/ui/button";
import { ChevronLeft } from "lucide-react";
import { usePathname } from "next/navigation";
import Link from "next/link";

const NavBar = () => {
  const pathname = usePathname();
  // Main navigation items
  const items = [
    { id: uuidv4(), title: "Overview", href: "/" },
    { id: uuidv4(), title: "Missing values", href: "/missingValues" },
    {
      id: uuidv4(),
      title: "Imputation",
      href: "/imputation/sinecosine/vmadjourNew",
    },
    {
      id: uuidv4(),
      title: "Data visualization",
      href: "/dataVisualisation/boxplot",
    },
    { id: uuidv4(), title: "Raw CSV", href: "/rawCSV" },
  ];

  // Sub-navigation items for specific sections
  const subNavItems = {
    imputation: [],
    dataVisualisation: [
      { id: uuidv4(), title: "Box Plot", href: "/dataVisualisation/boxplot" },
      {
        id: uuidv4(),
        title: "Histograms",
        href: "/dataVisualisation/histograms",
      },
      {
        id: uuidv4(),
        title: "Hierarchical Classification",
        href: "/dataVisualisation/hierarchical",
      },
      { id: uuidv4(), title: "Z-Score", href: "/dataVisualisation/zscore" },
    ],
  };

  const subsubnav = {
    sinecosine: [
      {
        id: uuidv4(),
        title: "V Badache",
        href: "/imputation/sinecosine/vbadache",
      },
      {
        id: uuidv4(),
        title: "V Badache New",
        href: "/imputation/sinecosine/vbadacheNew",
      },
      {
        id: uuidv4(),
        title: "V Madjour",
        href: "/imputation/sinecosine/vmadjourNew",
      },
      {
        id: uuidv4(),
        title: "V Benyelles",
        href: "/imputation/sinecosine/vbenyelles",
      },
      {
        id: uuidv4(),
        title: "V Bennebi",
        href: "/imputation/sinecosine/vbennebi",
      },
      {
        id: uuidv4(),
        title: "V Rzaiguia",
        href: "/imputation/sinecosine/vrzaiguia",
      },
      {
        id: uuidv4(),
        title: "V Salah",
        href: "/imputation/sinecosine/varab",
      }
    ],

  };

  return (
    <div className="flex items-center justify-center gap-2.5">
      {subNavItems[pathname.split("/")[1]] ? (
        // Sub-navigation view
        subsubnav[pathname.split("/")[2]] ? (
          <>
            <Link href="/">
              <Button>
                <ChevronLeft
                  style={{ width: "24px", height: "24px" }}
                  strokeWidth={1.5}
                />
              </Button>
            </Link>
            {subsubnav[pathname.split("/")[2]].map((item) => (
              <NavBtn href={item.href} key={item.id} title={item.title} />
            ))}
          </>
        ) : (
          <>
            <Link href="/">
              <Button>
                <ChevronLeft
                  style={{ width: "24px", height: "24px" }}
                  strokeWidth={1.5}
                />
              </Button>
            </Link>
            {subNavItems[pathname.split("/")[1]].map((item) => (
              <NavBtn href={item.href} key={item.id} title={item.title} />
            ))}
          </>
        )
      ) : (
        // Main navigation view
        items.map((item) => (
          <NavBtn key={item.id} title={item.title} href={item.href} />
        ))
      )}
    </div>
  );
};

export default NavBar;
