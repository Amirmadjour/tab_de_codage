"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache";
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import { Line } from 'react-chartjs-2';
import { motion } from "framer-motion";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import 'katex/dist/katex.min.css';
import { InlineMath } from 'react-katex';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const formatPolynomialEquation = (info) => {
  const { coefficients, intercept, feature_names } = info;
  let equation = `${intercept.toFixed(2)}`;
  
  for (let i = 1; i < coefficients.length; i++) {
    const coef = coefficients[i];
    if (coef !== 0) {
      const sign = coef > 0 ? " + " : " - ";
      const feature = feature_names[i]
        .replace('x0', 'x')
        .replace(/x(\d+)/, 'x_{$1}');
      equation += `${sign}${Math.abs(coef).toFixed(2)}${feature}`;
    }
  }
  
  return equation;
};

const page = () => {
  const getregression = async () => {
    const { data } = await axios.get("/polynomial/", { timeout: 300000 });
    return data;
  };

  const polynomial = useQuery({
    queryKey: ["polynomial"],
    queryFn: () => getregression(),
  });

  if (polynomial.isLoading) return <div><SkeletonTable /></div>;
  if (polynomial.isError) return <div className="text-red-400">{polynomial.error.message}</div>;
  if (!polynomial.data) return <div className="text-red-400">No data available.</div>;

  const plotInfo = polynomial.data.plot_info;
  const imputedData = JSON.parse(polynomial.data.dataset_imputed);

  if (!plotInfo || Object.keys(plotInfo).length === 0) {
    return <div className="text-red-400">Plot information is missing.</div>;
  }

  const combinedMseData = {
    labels: plotInfo[Object.keys(plotInfo)[0]].x_values,
    datasets: Object.entries(plotInfo).map(([column, info]) => ({
      label: `MSE pour ${column}`,
      data: info.y_values,
      borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`,
      backgroundColor: `hsla(${Math.random() * 360}, 70%, 50%, 0.2)`,
      fill: false,
    }))
  };

  const mseConfig = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'MSE en fonction du degré du polynôme pour toutes les colonnes'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'MSE'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Degré du polynôme'
        }
      }
    }
  };

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <div className="space-y-6 p-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Graphique MSE */}
        <div className="bg-white p-4 rounded-lg shadow h-[400px]">
          <Line 
            data={combinedMseData} 
            options={{
              ...mseConfig,
              maintainAspectRatio: false,
            }} 
          />
        </div>

        {/* Informations des colonnes */}
        <motion.div 
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 gap-4 auto-rows-min content-start"
        >
          {Object.entries(plotInfo).map(([column, info]) => (
            <motion.div
              key={column}
              variants={item}
              className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
            >
              <div className="bg-gradient-to-r from-blue-500 to-purple-500 -m-4 mb-4 p-4 rounded-t-lg">
                <h3 className="text-lg font-bold text-white">{column}</h3>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Degré optimal:</span>
                  <span className="font-semibold text-blue-600">{info.optimal_degree}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">MSE minimal:</span>
                  <span className="font-semibold text-purple-600">
                    {Math.min(...info.y_values).toFixed(4)}
                  </span>
                </div>
                <div className="mt-4">
                  <span className="text-gray-600">Équation:</span>
                  <div className="mt-2 p-2 bg-gray-50 rounded-md overflow-x-auto">
                    <InlineMath>{`y = ${formatPolynomialEquation(info)}`}</InlineMath>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-4 rounded-lg shadow"
      >
        <h3 className="text-lg font-semibold mb-4">Données imputées</h3>
        <div className="overflow-x-auto w-full">
          <div className="w-full">
            <SingleTableBadache 
              content={imputedData} 
              className="border-collapse w-full"
            />
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default page;
