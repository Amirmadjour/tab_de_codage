import LogoSVG from "@/app/assets/LogoSVG";
import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";
import NavBar from "@/app/components/NavBar";

const Header = () => {
  return (
    <div className="w-full h-fit p-2.5 flex items-center justify-between">
      <div className="flex items-center justify-between w-[300px]">
        <LogoSVG />
        <span>2.0v</span>
      </div>
      <NavBar />
      <div className="w-[300px] h-fit flex items-center justify-end">
        <Button>
          <Search
            style={{ width: "24px", height: "24px" }}
            strokeWidth={1.5}
            className="text-foreground-secondary"
          />
        </Button>
      </div>
    </div>
  );
};

export default Header;
