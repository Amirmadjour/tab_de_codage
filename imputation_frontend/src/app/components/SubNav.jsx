"use client";
import Link from "next/link";
import { v4 as uuidv4 } from "uuid";
import { usePathname } from "next/navigation";
import { useEffect } from "react";
import NavBtn from "@/app/components/NavBtn";

const SubNav = ({ menu }) => {
  const pathname = usePathname();

  useEffect(() => {
    console.log(pathname.slice(1));
  }, [pathname]);


  return (
    <ul className="flex space-x-4 p-2">
      {subNavItems[pathname.slice(1)]?.map((item) => (
        <NavBtn href={item.href} key={item.id} title={item.title} />
      ))}
    </ul>
  );
};

export default SubNav;
