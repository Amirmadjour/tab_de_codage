"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache"; // Vous pourriez envisager de le renommer en SingleTable si c'est générique
import { SkeletonTable } from "@/app/components/SkeletonComponent";
// import { Line, PolarArea } from 'react-chartjs-2'; // Commenté car les données ne correspondent pas
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   RadialLinearScale,
//   ArcElement,
//   Title,
//   Tooltip,
//   Legend
// } from 'chart.js';
import { motion } from 'framer-motion';

// ChartJS.register( // Commenté car les graphiques ne sont pas utilisés pour l'instant
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   RadialLinearScale,
//   ArcElement,
//   Title,
//   Tooltip,
//   Legend
// );

const MetricsCard = ({ title, value, suffix = '', highlight = false, highlightRed = false }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    className={`p-4 rounded-lg shadow-lg ${
        highlight
          ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white' 
          : highlightRed
          ? 'bg-red-500 text-white'
          : 'bg-white text-gray-700'
      }`}
  >
    <h3 className="text-sm font-medium opacity-80">{title}</h3>
    <div className="mt-2 flex items-baseline">
      <motion.span
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ 
          type: "spring",
          stiffness: 260,
          damping: 20,
          delay: 0.1 
        }}
        className="text-2xl font-bold"
      >
        {typeof value === 'number' ? Number(value).toFixed(2) : value}
      </motion.span>
      <span className="ml-1 text-sm opacity-80">{suffix}</span>
    </div>
  </motion.div>
);

// const ChartContainer = ({ title, children }) => ( // Commenté car les graphiques ne sont pas utilisés
//   <motion.div
//     initial={{ opacity: 0, y: 20 }}
//     animate={{ opacity: 1, y: 0 }}
//     transition={{ duration: 0.6 }}
//     className="bg-white p-6 rounded-xl shadow-lg"
//   >
//     <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">
//       {title}
//     </h3>
//     {children}
//   </motion.div>
// );

const SalahHybridImputationPage = () => {
  const getSalahHybridImputation = async () => {
    try {
      // La nouvelle API est un POST
      const { data } = await axios.post("/salah-hybrid-imputation/", {});
      return {
        ...data,
        dataset_imputed: JSON.parse(data.dataset_imputed), // dataset_imputed est déjà une chaîne JSON
        missing_mask: data.missing_mask
      };
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error(error.response?.data?.error || "Veuillez d'abord uploader un fichier CSV");
      }
      throw error; 
    }
  };

  const hybridQuery = useQuery({
    queryKey: ["salah-hybrid-imputation"], // Clé de query unique
    queryFn: getSalahHybridImputation,
    refetchOnWindowFocus: false,
    refetchOnMount: true,
    refetchOnReconnect: false,
    retry: 1,
  });

  if (hybridQuery.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (hybridQuery.isError)
    return <div className="text-red-400">{hybridQuery.error.message}</div>;
  if (!hybridQuery.data) return null;

  // Les données pour les graphiques Line et PolarArea ne sont pas disponibles dans le même format.
  // const chartConfig = createChartConfig( ... ); 
  // const polarConfig = createPolarConfig( ... );

  console.log('Query Data for Salah Hybrid Imputation:', hybridQuery.data);

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Métriques globales de l'Imputation Hybride (Salah)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"> {/* Ajusté le nombre de colonnes */}
          {hybridQuery.data.accuracy !== undefined && (
            <MetricsCard 
              title="Accuracy KNN (Test Split)" 
              value={hybridQuery.data.accuracy * 100}
              suffix="%"
              highlight={true}
            />
          )}
          {hybridQuery.data.overall_metrics && hybridQuery.data.overall_metrics["final_objective_value (1-accuracy)"] !== undefined && (
            <MetricsCard 
              title="Valeur Objective Finale" 
              value={hybridQuery.data.overall_metrics["final_objective_value (1-accuracy)"]}
              suffix="(1-Accuracy)"
            />
          )}
          {hybridQuery.data.duree !== undefined && (
            <MetricsCard
              title="Durée d'exécution"
              value={parseFloat(hybridQuery.data.duree)} // Assurer que c'est un nombre
              suffix="secondes"
              highlightRed={true}
            />
          )}
        </div>
        {hybridQuery.data.message && (
          <p className="mt-4 text-blue-600 bg-blue-100 p-3 rounded-md">{hybridQuery.data.message}</p>
        )}
      </div>

      {/* Les sections de graphiques sont commentées car les données ne sont pas au format attendu */}
      {/* <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ChartContainer title="Évolution de la Performance">
          <div className="w-full h-[400px]">
            <Line {...chartConfig} />
          </div>
          <p className="text-sm text-gray-600 mt-2 text-center">
            Suivi de la précision et du MSE au fil des époques
          </p>
        </ChartContainer>

        <ChartContainer title="Distribution des F-Scores">
          <div className="w-full h-[400px]">
            <PolarArea {...polarConfig} />
          </div>
          <p className="text-sm text-gray-600 mt-2 text-center">
            Performance d'imputation par colonne
          </p>
        </ChartContainer>
      </div> */}

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg overflow-hidden"
      >
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">
            Données Imputées (Hybride Salah)
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Résultats de l'imputation avec l'algorithme Hybride SCA-GWO
          </p>
        </div>
        <div className="p-4">
          <SingleTableBadache 
            content={hybridQuery.data.dataset_imputed}
            missingMask={hybridQuery.data.missing_mask}
            className="border-collapse w-full"
          />
        </div>
      </motion.div>
    </div>
  );
};

export default SalahHybridImputationPage;