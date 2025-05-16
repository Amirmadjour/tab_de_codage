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
          ? 'bg-gradient-to-r from-teal-500 to-teal-600 text-white' // Nouvelle couleur pour Benyelles Full
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
        {typeof value === 'number' ? Number(value).toFixed(3) : (typeof value === 'string' && value.length > 30 ? value.substring(0,27) + "..." : value) }
      </motion.span>
      <span className="ml-1 text-xs opacity-80">{suffix}</span>
    </div>
  </motion.div>
);

const FeatureListCard = ({ title, features }) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay: 0.1 }}
    className="p-4 rounded-lg shadow-lg bg-white text-gray-700 col-span-1 md:col-span-2" // Prend plus de largeur
  >
    <h3 className="text-sm font-medium opacity-80 mb-2">{title}</h3>
    {features && features.length > 0 ? (
      <ul className="list-disc list-inside space-y-1 text-xs max-h-32 overflow-y-auto">
        {features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
    ) : (
      <p className="text-xs text-gray-500">Aucune feature sélectionnée ou applicable.</p>
    )}
  </motion.div>
);


const BenyellesFullImputationPage = () => {
  const getBenyellesFullData = async () => {
    try {
      // L'URL de l'API a été mise à jour pour refléter la nouvelle vue/logique
      const { data } = await axios.post("/benyelles-sca-gwo-imputation/", {}); 
      // dataset_imputed est déjà une chaîne JSON du backend
      if (typeof data.dataset_imputed === 'string') {
        data.dataset_imputed = JSON.parse(data.dataset_imputed);
      }
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Erreur lors du chargement des données d'imputation.";
      console.error("Erreur lors de la récupération des données d'imputation de Benyelles (Full):", error);
      throw new Error(errorMessage);
    }
  };

  const benyellesQuery = useQuery({
    queryKey: ["benyelles-sca-gwo-imputation"], // Clé de query mise à jour
    queryFn: getBenyellesFullData,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
    staleTime: 1000 * 60 * 60* 60,
    retry: 1,
  });

  if (benyellesQuery.isLoading) return <div><SkeletonTable /></div>;
  if (benyellesQuery.isError) return <div className="text-red-400 p-4 bg-red-100 rounded-md">{benyellesQuery.error.message}</div>;
  if (!benyellesQuery.data) return <div className="p-4">Aucune donnée à afficher.</div>;

  const { data } = benyellesQuery;
  console.log('Query Data for Benyelles SCA-GWO Imputation:', data);

  const selectedFeatures = data.selected_features_info?.selected_feature_names || [];

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Métriques de l'Imputation SCA-GWO (Benyelles)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.accuracy_value !== undefined && (
            <MetricsCard 
              title={`Accuracy (${data.accuracy_type || 'N/A'})`}
              value={data.accuracy_value * 100}
              suffix="%"
              highlight={true}
            />
          )}
          {data.selected_features_info?.num_selected_features !== undefined && (
            <MetricsCard 
              title="Features Sélectionnées (GWO)" 
              value={data.selected_features_info.num_selected_features}
              suffix="features"
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
           {data.selected_features_info && (
             <FeatureListCard title="Noms des Features Sélectionnées" features={selectedFeatures} />
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
            Meilleur Dataset Imputé (SCA-GWO Benyelles)
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Dataset résultant de la meilleure combinaison d'imputation SCA et de sélection de features GWO.
          </p>
        </div>
        <div className="p-4">
          {data.dataset_imputed && data.missing_mask ? (
            <SingleTableBadache 
              content={data.dataset_imputed}
              missingMask={data.missing_mask}
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

export default BenyellesFullImputationPage;