"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache"; 
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import { motion } from 'framer-motion';

const MetricsCard = ({ title, value, suffix = '', highlight = false, highlightRed = false, smallText = false }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    className={`p-4 rounded-lg shadow-lg ${
        highlight
          ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white' // Nouvelle couleur pour Radhi/Badache
          : highlightRed
          ? 'bg-red-500 text-white'
          : 'bg-white text-gray-700'
      }`}
  >
    <h3 className={`text-sm font-medium opacity-80 ${smallText ? 'mb-1' : ''}`}>{title}</h3>
    <div className="mt-1 flex items-baseline">
      <motion.span
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ 
          type: "spring",
          stiffness: 260,
          damping: 20,
          delay: 0.1 
        }}
        className={`${smallText ? 'text-lg' : 'text-2xl'} font-bold`}
      >
        {typeof value === 'number' ? Number(value).toFixed(3) : (typeof value === 'string' && value.length > 25 ? value.substring(0,22) + "..." : value) }
      </motion.span>
      <span className="ml-1 text-xs opacity-80">{suffix}</span>
    </div>
  </motion.div>
);


const RadhiImputationPage = () => {
  const getRadhiData = async () => {
    try {
      const { data } = await axios.post("/radhi-sca-gwo-imputation/", {}); 
      if (data.dataset_imputed && typeof data.dataset_imputed === 'string') {
        data.dataset_imputed = JSON.parse(data.dataset_imputed);
      }
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Erreur lors du chargement des données d'imputation de Radhi.";
      console.error("Erreur API Radhi:", error);
      throw new Error(errorMessage);
    }
  };

  const radhiQuery = useQuery({
    queryKey: ["radhi-sca-gwo-imputation"], 
    queryFn: getRadhiData,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
    staleTime: 1000 * 60 * 60*60,
    retry: 1,
  });

  if (radhiQuery.isLoading) return <div><SkeletonTable /></div>;
  if (radhiQuery.isError) return <div className="text-red-400 p-4 bg-red-100 rounded-md">{radhiQuery.error.message}</div>;
  
  const { data } = radhiQuery;
  if (!data || !data.dataset_imputed) { 
      return <div className="p-4">{data?.message || "Aucune donnée valide à afficher pour Radhi."}</div>;
  }

  console.log('Query Data for Radhi SCA-GWO Imputation:', data);

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Résultats de l'Imputation (Radhi SCA-GWO Mealpy)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.final_accuracy_knn !== undefined && (
            <MetricsCard 
              title="Accuracy Finale (KNN)"
              value={data.final_accuracy_knn * 100}
              suffix="%"
              highlight={true}
            />
          )}
          {data.duree !== undefined && (
            <MetricsCard
              title="Durée d'exécution"
              value={parseFloat(data.duree)} 
              suffix="secondes"
              highlightRed={true}
            />
          )}
        </div>
        {data.message && (
          <p className="mt-4 text-blue-600 bg-blue-100 p-3 rounded-md">{data.message}</p>
        )}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg overflow-hidden"
      >
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">
            Dataset Imputé (Radhi)
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Dataset résultant de l'imputation par l'algorithme hybride SCA-GWO utilisant Mealpy.
          </p>
        </div>
        <div className="p-4">
          {data.dataset_imputed && data.original_missing_mask ? (
            <SingleTableBadache 
              content={data.dataset_imputed}
              missingMask={data.original_missing_mask} 
              className="border-collapse w-full"
            />
          ) : (
            <p>Les données imputées ne sont pas disponibles.</p>
          )}
        </div>
      </motion.div>
      
      
      
    </div>
  );
};

export default RadhiImputationPage;