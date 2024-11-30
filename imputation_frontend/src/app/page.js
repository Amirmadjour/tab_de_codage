"use client";
import InfoCard from "@/app/components/InfoCard";
import DangerCard from "./components/DangerCard";
import FileUpload from "./components/FileUpload";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  FileCheck,
  FileMinus,
  PaintBucket,
  ChartNoAxesCombined,
  File,
  FileWarning,
} from "lucide-react";

export default function Home() {
  const [notification, setNotification] = useState(false);

  const variants = {
    hidden: { opacity: 0, x: 150 }, // Initial state: hidden and shifted down
    visible: { opacity: 1, x: 0 }, // Final state: fully visible and in position
  };

  return (
    <div className="h-full w-full flex items-start justify-center p-2.5 overflow-hidden">
      <div className="max-h-full shrink-0 overflow-y-auto flex flex-col items-center gap-2.5 justify-start">
        <span className="w-full text-2xl font-semibold">Guidelines</span>
        <DangerCard
          title="Your file"
          time="1 seconde ago"
          description="Make sure the file you upload is CSV"
          icon={<FileWarning className="text-white" />}
        />
        <span className="w-full text-2xl font-semibold">Traitement</span>
        <InfoCard
          title="Missing Values"
          time="1min ago"
          description="Know how much you missed a shot"
          icon={<FileMinus className="text-foreground-secondary" />}
        />
        <InfoCard
          title="Imputation"
          time="1min ago"
          description="Fill them missing values"
          icon={<PaintBucket className="text-foreground-secondary" />}
        />
        <InfoCard
          title="Data visualisation"
          time="1min ago"
          description="The visual representation of your file"
          icon={<ChartNoAxesCombined className="text-foreground-secondary" />}
        />
        <InfoCard
          title="Raw CSV"
          time="1min ago"
          description="You can view your file"
          icon={<File className="text-foreground-secondary" />}
        />
      </div>
      <FileUpload setNotification={() => setNotification(true)} />
      {notification && (
        <motion.div
          initial="hidden" // Starting animation state
          animate="visible" // State to animate to
          variants={variants} // Animation variants
          transition={{ duration: 0.8, ease: "circOut" }} // Animation timing
          className="max-h-full overflow-y-auto shrink-0 flex flex-col items-center gap-2.5 justify-start"
        >
          <span className="w-full text-2xl font-semibold">Guidelines</span>
          <InfoCard
            title="Success"
            time="1 seconde ago"
            description="Your file was upload successfully"
            icon={<FileCheck className="text-foreground-secondary" />}
            strip_variant="success"
          />
        </motion.div>
      )}
    </div>
  );
}
