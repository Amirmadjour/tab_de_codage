"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

const NavBtn = ({ title, href }) => {
  return (
    <Link href={href}>
      <Button className="font-medium text-lg px-6 leading-[24px]">
        {title}
      </Button>
    </Link>
  );
};

export default NavBtn;
