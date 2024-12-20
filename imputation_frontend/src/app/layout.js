"use client";
import localFont from "next/font/local";
import "./globals.css";
import Header from "@/app/components/Header";
import { RawDataProvider } from "@/lib/RawDataContext";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

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

export default function RootLayout({ children }) {
  const queryClient = new QueryClient();
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${interVariable.className} antialiased w-screen h-screen flex flex-col items-center justify-center gap-2.5 p-2.5`}
      >
        <QueryClientProvider client={queryClient}>
          <RawDataProvider>
            <Header />
            <div className="grow overflow-auto w-full">{children}</div>
          </RawDataProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
