import InfoCard from "@/app/components/InfoCard";
import DangerCard from "./components/DangerCard";
import FileUpload from "./components/FileUpload";

export default function Home() {
  return (
    <div className="h-full w-full flex items-start justify-center p-2.5">
      <div className="max-h-full shrink-0 overflow-y-auto flex flex-col items-center gap-2.5 justify-start">
        <span className="w-full text-2xl font-semibold">Guidelines</span>
        <DangerCard
          title="Your file"
          time="1 seconde ago"
          description="Make sure the file you upload is CSV"
        />
        <span className="w-full text-2xl font-semibold">Traitement</span>
        <InfoCard
          title="Missing Values"
          time="1min ago"
          description="Know how much you missed a shot"
        />
        <InfoCard
          title="Imputation"
          time="1min ago"
          description="Fill them missing values"
        />
        <InfoCard
          title="Data visualisation"
          time="1min ago"
          description="The visual representation of your file"
        />
        <InfoCard
          title="Raw CSV"
          time="1min ago"
          description="You can view your file"
        />
      </div>
      <FileUpload />
      <div className="max-h-full overflow-y-auto shrink-0 flex flex-col items-center gap-2.5 justify-start">
        <span className="w-full text-2xl font-semibold">Guidelines</span>
        <DangerCard
          title="Your file"
          time="1 seconde ago"
          description="Make sure the file you upload is CSV"
        />
      </div>
    </div>
  );
}
