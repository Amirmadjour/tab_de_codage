"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const NavBtn = ({ title, href }) => {
  const pathname = usePathname();
  return (
    <Link href={href}>
      <Button
        className={clsx(
          "font-medium text-lg px-6 leading-[24px]",
          pathname == href && "bg-accent text-accent-foreground hover:bg-accent/85"
        )}
      >
        {title}
      </Button>
    </Link>
  );
};

export default NavBtn;
