"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache";
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import { Line, PolarArea } from 'react-chartjs-2';
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
import { motion } from 'framer-motion';

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

const MetricsCard = ({ title, value, suffix = '', highlight = false, highlightRed=false }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    //className={`p-6 rounded-lg shadow-lg ${
    //  highlight
     //   ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
      //  : 'bg-white'
    //}`}
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
        {Number(value).toFixed(2)}
      </motion.span>
      <span className="ml-1 text-sm opacity-80">{suffix}</span>
    </div>
  </motion.div>
);

const ChartContainer = ({ title, children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    className="bg-white p-6 rounded-xl shadow-lg"
  >
    <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">
      {title}
    </h3>
    {children}
  </motion.div>
);

const ScaPage = () => {
  const getScaImputation = async () => {
    try {
      const { data } = await axios.get("/sca_radi/");
      return {
        ...data,
        dataset_imputed: JSON.parse(data.dataset_imputed),
        missing_mask: data.missing_mask
      };
    } catch (error) {
      // Si l'erreur est 400, c'est probablement qu'aucun fichier n'a été uploadé
      if (error.response?.status === 400) {
        throw new Error("Veuillez d'abord uploader un fichier CSV");
      }
      throw error; // Relancer les autres erreurs
    }
  };

  const scaQuery = useQuery({
    queryKey: ["sca-imputation"],
    queryFn: () => getScaImputation(),
    refetchOnWindowFocus: false,
    refetchOnMount: true,
    refetchOnReconnect: false,
    retry: 1,
  });

  const createChartConfig = (accuracyData, fitnessData) => {
    const labels = Array.from({length: accuracyData.length}, (_, i) => i + 1);
    const totalDuration = 10000;
    const delayBetweenPoints = totalDuration / accuracyData.length;

    const previousY = (ctx) => ctx.index === 0
      ? ctx.chart.scales.y.getPixelForValue(100)
      : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;

    const animation = {
      x: {
        type: 'number',
        easing: 'linear',
        duration: delayBetweenPoints,
        from: NaN,
        delay(ctx) {
          if (ctx.type !== 'data' || ctx.xStarted) {
            return 0;
          }
          ctx.xStarted = true;
          return ctx.index * delayBetweenPoints;
        }
      },
      y: {
        type: 'number',
        easing: 'linear',
        duration: delayBetweenPoints,
        from: previousY,
        delay(ctx) {
          if (ctx.type !== 'data' || ctx.yStarted) {
            return 0;
          }
          ctx.yStarted = true;
          return ctx.index * delayBetweenPoints;
        }
      }
    };

    return {
      data: {
        labels,
        datasets: [
          {
            label: 'Accuracy',
            data: accuracyData,
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1,
            radius: 0,
          },
          {
            label: 'Fitness MSE',
            data: fitnessData,
            borderColor: 'rgb(53, 162, 235)',
            borderWidth: 1,
            radius: 0,
          }
        ]
      },
      options: {
        animation,
        interaction: {
          intersect: false
        },
        plugins: {
          legend: {
            display: true
          }
        },
        scales: {
          x: {
            type: 'linear',
            title: {
              display: true,
              text: 'Epochs'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Value'
            }
          }
        }
      }
    };
  };

  const createPolarConfig = (metrics) => {
    const columns = Object.keys(metrics);
    const fScores = columns.map(col => metrics[col].f_score);

    return {
      data: {
        labels: columns,
        datasets: [
          {
            label: 'F-Score par colonne',
            data: fScores,
            backgroundColor: [
              'rgba(255, 99, 132, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 206, 86, 0.5)',
              'rgba(75, 192, 192, 0.5)',
              'rgba(153, 102, 255, 0.5)',
              'rgba(255, 159, 64, 0.5)',
            ],
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            pointLabels: {
              display: true,
              centerPointLabels: true,
              font: {
                size: 12
              }
            },
            beginAtZero: true,
            max: 1,
            ticks: {
              backdropPadding: 3
            }
          }
        },
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'F-Score des colonnes imputées'
          }
        }
      }
    };
  };

  if (scaQuery.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (scaQuery.isError)
    return <div className="text-red-400">{scaQuery.error.message}</div>;
  if (!scaQuery.data) return null;

  const chartConfig = createChartConfig(
    scaQuery.data.accuracy,
    scaQuery.data.fitness_mse
  );

  const polarConfig = createPolarConfig(scaQuery.data.metrics);

  console.log('Query Data:', scaQuery.data);

  return (
    <div className="space-y-8 p-6">
      <div className="bg-gray-50 p-6 rounded-xl">
        <motion.h2 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl font-bold mb-4 text-gray-800"
        >
          Métriques globales
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <MetricsCard 
            title="MSE Initial" 
            value={scaQuery.data.overall_metrics.initial_mse}
            suffix="mse"
          />
          <MetricsCard 
            title="MSE Final" 
            value={scaQuery.data.overall_metrics.final_mse}
            suffix="mse"
          />
          <MetricsCard 
            title="Maximale Accuracy"
            value={scaQuery.data.overall_metrics.max_accuracy * 100}
            suffix="%"
            highlight={true}
          />
          <MetricsCard 
            title="Amélioration Totale" 
            value={scaQuery.data.overall_metrics.total_improvement}
            suffix="%"
          />
          <MetricsCard
            title="Durée d'execution"
            value={scaQuery.data.duree}
            suffix="seconde"
            highlightRed={true}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg overflow-hidden"
      >
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">
            Données Imputées
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Résultats de l'imputation avec l'algorithme SCA
          </p>
        </div>
        <div className="p-4">
          <SingleTableBadache 
            content={scaQuery.data.dataset_imputed}
            missingMask={scaQuery.data.missing_mask}
            className="border-collapse w-full"
          />
        </div>
      </motion.div>
    </div>
  );
};

export default ScaPage;