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
      href: "/imputation/knn",
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
    imputation: [
      { id: uuidv4(), title: "KNN", href: "/imputation/knn" },
      { id: uuidv4(), title: "Linear Regression", href: "/imputation/linear" },
      {
        id: uuidv4(),
        title: "Polynomial Regression",
        href: "/imputation/polynomial",
      },
      {
        id: uuidv4(),
        title: "Sine Cosine Algorithm",
        href: "/imputation/sinecosine/vbadache",
      },
    ],
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
        title: "Version Badache",
        href: "/imputation/sinecosine/vbadache",
      },
      {
        id: uuidv4(),
        title: "Version Madjour",
        href: "/imputation/sinecosine/vmadjour",
      },
    ],
  };

  console.log(pathname.split("/")[2]);

  return (
    <div className="flex items-center justify-center gap-2.5">
      {subNavItems[pathname.split("/")[1]] ? (
        // Sub-navigation view
        subsubnav[pathname.split("/")[2]] ? (
          <>
            <Link href="/imputation/knn">
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
