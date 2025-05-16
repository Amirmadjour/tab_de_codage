"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache"; 
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import { motion } from 'framer-motion';


const MetricsCard = ({ title, value, suffix = '', highlight = false, highlightRed = false }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    className={`p-4 rounded-lg shadow-lg ${
        highlight
          ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white' // Couleur différente pour cette page
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

const AmirImputationPage = () => {
  const getAmirImputationData = async () => {
    try {
      const { data } = await axios.post("/amir-sca-gwo-imputation/", {}); // Envoyer un corps vide si aucun paramètre n'est requis
      if (typeof data.dataset_imputed === 'string') {
        data.dataset_imputed = JSON.parse(data.dataset_imputed);
      }
      return data;
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error(error.response?.data?.error || "Veuillez d'abord uploader un fichier CSV");
      }
      console.error("Erreur lors de la récupération des données d'imputation d'Amir:", error);
      throw new Error(error.response?.data?.error || "Erreur lors du chargement des données d'imputation.");
    }
  };

  const amirQuery = useQuery({
    queryKey: ["amir-sca-gwo-imputation"],
    queryFn: getAmirImputationData,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
    staleTime: 1000 * 60 * 60 * 60,
    retry: 1,
  });

  if (amirQuery.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (amirQuery.isError)
    return <div className="text-red-400 p-4 bg-red-100 rounded-md">{amirQuery.error.message}</div>;
  if (!amirQuery.data) return <div className="p-4">Aucune donnée à afficher.</div>;

  console.log('Query Data for Amir SCA-GWO Imputation:', amirQuery.data);

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Métriques de l'Imputation SCA-GWO (Madjour)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {amirQuery.data.accuracy !== undefined && (
            <MetricsCard 
              title="Accuracy KNN (après SCA-GWO)" 
              value={amirQuery.data.accuracy * 100}
              suffix="%"
              highlight={true}
            />
          )}
          {amirQuery.data.metrics && amirQuery.data.metrics.final_sca_objective_value !== undefined && (
            <MetricsCard 
              title="Valeur Objective Finale SCA" 
              value={amirQuery.data.metrics.final_sca_objective_value}
              suffix="(1-Accuracy GWO)"
            />
          )}
          {amirQuery.data.duree !== undefined && (
            <MetricsCard
              title="Durée d'exécution"
              value={parseFloat(amirQuery.data.duree)} 
              suffix="secondes"
              highlightRed={true}
            />
          )}
        </div>
        {amirQuery.data.metrics && amirQuery.data.metrics.message && (
          <p className="mt-4 text-blue-600 bg-blue-100 p-3 rounded-md">{amirQuery.data.metrics.message}</p>
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
            Données Imputées (SCA-GWO Madjour)
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Résultats de l'imputation avec l'algorithme SCA-GWO de Madjour.
          </p>
        </div>
        <div className="p-4">
          {amirQuery.data.dataset_imputed && amirQuery.data.missing_mask ? (
            <SingleTableBadache 
              content={amirQuery.data.dataset_imputed} // Doit être l'objet parsé
              missingMask={amirQuery.data.missing_mask}
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

export default AmirImputationPage;