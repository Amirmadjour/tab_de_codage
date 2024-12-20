import localFont from "next/font/local";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import SideBar from "@/components/SideBar";
import BreadCrumb from "@/components/BreadCrumb";
import { DataProvider } from "@/components/DataContext";
import { RawDataProvider } from "@/components/RawDataContext";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

const interVariable = localFont({
  src: [
    {
      path: "./fonts/InterVariable.woff2",
      style: "normal",
    },
    {
      path: "./fonts/InterVariable-Italic.woff2",
      style: "italic",
    },
  ],
  variable: "--font-inter-variable", // Optional CSS variable
  display: "swap",
});

export const metadata = {
  title: "Radhi madjour",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${interVariable.className} antialiased bg-background w-screen h-screen overflow-hidden`}
      >
        <div className="w-full h-full  flex items-center justify-center gap-2.5 p-2.5 font-medium">
          <SideBar />
          <RawDataProvider>
            <DataProvider>
              <div className="flex flex-col items-start justify-start px-5 py-2.5 gap-1 h-full grow bg-background-secondary rounded-[20px] shadow-[0_0_4px_0_rgba(0,0,0,0.25)] overflow-auto">
                <BreadCrumb />
                {children}
              </div>
            </DataProvider>
          </RawDataProvider>
        </div>
        <Toaster />
      </body>
    </html>
  );
}
