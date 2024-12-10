"use client";
import { useState, useEffect, useRef } from "react";

const ResponsiveRectangle = () => {
  const svg = useRef(null);
  const path = useRef(null);
  const [size, setSize] = useState({
    svg: { width: 0, height: 0 },
    path: { width: 0, height: 0 },
  });

  useEffect(() => {
    // Get the element size when the component mounts
    if (svg.current) {
      const rect = svg.current.getBoundingClientRect();
      console.log(rect.height, rect.width);
      setSize((prev) => ({
        ...prev,
        svg: { width: rect.width, height: rect.height },
      }));
    }
    if (path.current) {
      const rect = path.current.getBoundingClientRect();
      console.log(rect.height, rect.width);
      setSize((prev) => ({
        ...prev,
        path: { width: rect.width, height: rect.height },
      }));
    }

    // Optional: Add a resize listener to update size dynamically
    const handleResize = () => {
      if (svg.current) {
        const rect = svg.current.getBoundingClientRect();
        setSize((prev) => ({
          ...prev,
          svg: { width: rect.width, height: rect.height },
        }));
      }
      if (path.current) {
        const rect = path.current.getBoundingClientRect();
        setSize((prev) => ({
          ...prev,
          path: { width: rect.width, height: rect.height },
        }));
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <svg
      ref={svg}
      xmlns="http://www.w3.org/2000/svg"
      style={{
        width: "100%",
        height: "100%",
      }}
      className="absolute"
    >
      <rect height="100%" width="100%" fill="#FFFFFF80" rx="16" ry="16" />
      <path
        ref={path}
        d="M3.00001 3.05176e-05C-36.9998 3.05176e-05 518 3.05176e-05 478 3.05176e-05C438 3.05176e-05 438 40 438 40C438 40 438 40 438 40V40C438 62.0914 420.091 80 398 80H82.9999C60.9086 80 43 62.0915 43 40.0001V40.0001C43 40.0001 43 40.0001 43 40C43 39.9979 42.9988 3.05176e-05 3.00001 3.05176e-05Z"
        fill={size.path.width != 0 ? "#F0F2F3" : "transparent"}
        transform={`translate(${-size.path.width / 2 + size.svg.width / 2}, 0)`}
      />
    </svg>
  );
};

export default ResponsiveRectangle;
