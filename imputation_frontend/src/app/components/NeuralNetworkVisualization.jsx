import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const NeuralNetworkVisualization = ({ width = 800, height = 400, architecture }) => {
  const svgRef = useRef();
  const [networkConfig, setNetworkConfig] = useState({
    inputLayerHeight: architecture?.input_layer || 15,
    hiddenLayersCount: architecture?.hidden_layers?.length || 2,
    hiddenLayersDepths: architecture?.hidden_layers || [10, 10, 10, 10, 10],
    outputLayerHeight: architecture?.output_layer || 5
  });

  const buildNodeGraph = () => {
    const nodes = [];
    
    // Input layer
    for (let i = 0; i < networkConfig.inputLayerHeight; i++) {
      nodes.push({ label: `i${i}`, layer: 1 });
    }

    // Hidden layers
    for (let hiddenLayerLoop = 0; hiddenLayerLoop < networkConfig.hiddenLayersCount; hiddenLayerLoop++) {
      for (let i = 0; i < networkConfig.hiddenLayersDepths[hiddenLayerLoop]; i++) {
        nodes.push({ label: `h${hiddenLayerLoop}${i}`, layer: hiddenLayerLoop + 2 });
      }
    }

    // Output layer
    for (let i = 0; i < networkConfig.outputLayerHeight; i++) {
      nodes.push({ label: `o${i}`, layer: networkConfig.hiddenLayersCount + 2 });
    }

    return { nodes };
  };

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current);
    const graph = buildNodeGraph();
    const nodes = graph.nodes;
    const nodeSize = 15;
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Calculate network size
    const netsize = {};
    nodes.forEach(d => {
      netsize[d.layer] = (netsize[d.layer] || 0) + 1;
    });

    // ... rest of the code ...
  }, [networkConfig]);

  return <svg ref={svgRef} width={width} height={height} />;
};

export default NeuralNetworkVisualization; 