"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache";
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import { Line, PolarArea } from 'react-chartjs-2';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  RadialLinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Enregistrement des composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  RadialLinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Composants réutilisables
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
        {isNaN(value) ? "N/A" : Number(value).toFixed(2)}
      </motion.span>
      <span className="ml-1 text-sm opacity-80">{suffix}</span>
    </div>
  </motion.div>
);

const ChartContainer = ({ title, children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white p-4 rounded-lg shadow"
  >
    <h2 className="text-xl font-bold mb-4">{title}</h2>
    <div className="h-[300px]">
      {children}
    </div>
  </motion.div>
);

const MLPPage = () => {
  const getMlp = async () => {
    try {
      const { data } = await axios.get("/mlp/");
      return {
        ...data,
        dataset_imputed: JSON.parse(data.dataset_imputed),
        missing_mask: data.missing_mask
      };
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error("Veuillez d'abord uploader un fichier CSV");
      }
      throw error;
    }
  };

  const mlp = useQuery({
    queryKey: ["mlp"],
    queryFn: getMlp,
    staleTime: Infinity,
  });

  if (!mlp.data) return <SkeletonTable />;
  if (mlp.isLoading) return <SkeletonTable />;
  if (mlp.isError) return <div className="text-red-400">{mlp.error.message}</div>;

  const overall_metrics = mlp.data?.overall_metrics || {};

  return (
    <div className="space-y-6 p-4">
      {/* Métriques globales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricsCard
          title="Précision de prédiction"
          value={overall_metrics.prediction_accuracy}
          suffix="%"
          highlight={true}
        />
        <MetricsCard
          title="F-Score Global"
          value={overall_metrics.global_f_score}
          highlight={false}
        />
        <MetricsCard
          title="Durée d'exécution"
          value={mlp.data.duree}
          suffix=" sec"
        />
        <MetricsCard
          title="Amélioration totale"
          value={overall_metrics.total_improvement}
          suffix="%"
          highlight={false}
        />
      </div>

      {/* Métriques par colonne */}
      <ChartContainer title="F-score par colonne">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-h-[120px] overflow-y-auto w-full p-2">
          {Object.entries(mlp.data.metrics).map(([column, metrics]) => (
            <MetricsCard
              key={column}
              title={metrics.column_name}
              value={metrics.f_score}
              highlightRed={metrics.f_score < 0.5}
              highlight={false}
              className="w-full h-16"
            />
          ))}
        </div>
      </ChartContainer>

      {/* Graphiques d'évolution */}
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <ChartContainer title="Évolution MSE">
          <Line
            data={{
              labels: mlp.data.fitness_mse.map((_, index) => `${index + 1}`),
              datasets: [{
                label: "MSE",
                data: mlp.data.fitness_mse,
                borderColor: "rgba(75,192,192,1)",
                fill: false,
              }],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Époque",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "MSE",
                  },
                  beginAtZero: true,
                },
              },
            }}
          />
        </ChartContainer>
        <ChartContainer title="Évolution de la précision">
          <Line
            data={{
              labels: mlp.data.accuracy.map((_, index) => `${index + 1}`),
              datasets: [
                {
                  label: "Précision",
                  data: mlp.data.accuracy,
                  borderColor: "rgba(153,102,255,1)",
                  fill: false,
                },
              ],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Époque",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "Précision",
                  },
                },
              },
            }}
          />
        </ChartContainer>
      </motion.div>

      {/* Tableau des données imputées */}
      <ChartContainer title="Données imputées">
        <SingleTableBadache
          content={mlp.data.dataset_imputed}
          missingMask={mlp.data.missing_mask}
          className="border-collapse w-full"
        />
      </ChartContainer>
    </div>
  );
};

export default MLPPage;