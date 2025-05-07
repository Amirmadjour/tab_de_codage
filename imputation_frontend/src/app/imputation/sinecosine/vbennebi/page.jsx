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
          ? 'bg-gradient-to-r from-cyan-500 to-cyan-600 text-white' // Couleur pour Bennebi
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

const FeatureListCard = ({ title, features }) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay: 0.1 }}
    className="p-4 rounded-lg shadow-lg bg-white text-gray-700 col-span-1 md:col-span-2"
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

const BennebiImputationPage = () => {
  const getBennebiData = async () => {
    try {
      const { data } = await axios.post("/bennebi-sca-gwo-imputation/", {}); 
      if (data.dataset_imputed_selected_features && typeof data.dataset_imputed_selected_features === 'string') {
        data.dataset_imputed_selected_features = JSON.parse(data.dataset_imputed_selected_features);
      }
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Erreur lors du chargement des données d'imputation de Bennebi.";
      console.error("Erreur API Bennebi:", error);
      throw new Error(errorMessage);
    }
  };

  const bennebiQuery = useQuery({
    queryKey: ["bennebi-sca-gwo-imputation"],
    queryFn: getBennebiData,
    refetchOnWindowFocus: false,
    refetchOnMount: true,
    refetchOnReconnect: false,
    retry: 1,
  });

  if (bennebiQuery.isLoading) return <div><SkeletonTable /></div>;
  if (bennebiQuery.isError) return <div className="text-red-400 p-4 bg-red-100 rounded-md">{bennebiQuery.error.message}</div>;
  
  const { data } = bennebiQuery;
  if (!data || !data.dataset_imputed_selected_features) { // Vérifier si les données essentielles sont là
      return <div className="p-4">{data?.message || "Aucune donnée valide à afficher pour Bennebi."}</div>;
  }

  console.log('Query Data for Bennebi SCA-GWO Imputation:', data);

  const imputationStrategy = data.best_imputation_strategy;
  const strategyDisplay = imputationStrategy ? 
    `${imputationStrategy.strategy}${imputationStrategy.fill_value !== null ? ` (val: ${Number(imputationStrategy.fill_value).toFixed(2)})` : ''}`
    : "N/A";

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Métriques de l'Optimisation (Bennebi SCA-GWO)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.best_accuracy_knn !== undefined && (
            <MetricsCard 
              title="Meilleure Accuracy KNN"
              value={data.best_accuracy_knn * 100}
              suffix="%"
              highlight={true}
            />
          )}
          {data.best_selected_feature_names && (
            <MetricsCard 
              title="Features Sélectionnées (GWO)" 
              value={data.best_selected_feature_names.length}
              suffix="features"
            />
          )}
           <MetricsCard 
              title="Stratégie d'Imputation" 
              value={strategyDisplay}
              smallText={true}
            />
          {data.duree !== undefined && (
            <MetricsCard
              title="Durée d'exécution"
              value={parseFloat(data.duree)} 
              suffix="secondes"
              highlightRed={true}
            />
          )}
           {data.best_selected_feature_names && data.best_selected_feature_names.length > 0 && (
             <FeatureListCard title="Noms des Features Sélectionnées" features={data.best_selected_feature_names} />
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
            Table Finale Imputée (Bennebi - Features Sélectionnées)
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Dataset résultant de la meilleure stratégie d'imputation et sélection de features, affichant uniquement les features sélectionnées et la cible.
          </p>
        </div>
        <div className="p-4">
          {data.dataset_imputed_selected_features && data.original_missing_mask ? (
            <SingleTableBadache 
              content={data.dataset_imputed_selected_features} // Ce dataset contient déjà uniquement les features sélectionnées + cible
              // Le missing_mask original est pour tout le dataset, donc il faut l'adapter ou l'ignorer pour ce tableau spécifique
              // Pour l'instant, on passe le masque original, SingleTableBadache devra être robuste.
              // Idéalement, on construirait un masque spécifique pour les colonnes affichées.
              missingMask={data.original_missing_mask} 
              className="border-collapse w-full"
            />
          ) : (
            <p>Les données imputées et sélectionnées ne sont pas disponibles.</p>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default BennebiImputationPage;