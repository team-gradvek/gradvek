import {
  Heading,
  Text,
  Card, CardBody, Box
} from '@chakra-ui/react'
import DataTableSkeleton from '../results/DataTableSkeleton'
// import 'react-loading-skeleton/dist/skeleton.css'
import getPathwayData from '@/hooks/pathwaysHook'
import { useState, useEffect, useRef } from 'react'
import ResultsLayout from '../results/ResultsLayout'
import vis from 'vis-network';
import { DataSet } from 'vis-data';
import { Network } from 'vis-network';



const PathsKG = ({title, data}) => {

  const graphRef = useRef(null);

  console.log(data)

  // Needs to be removed
  // const dataSlice = data.slice(0,200)

  const nodes = data.filter(item => item.group === "nodes").map(item => ({
    id: item.data.id, 
    label: item.data.name 
  }));

  const edges = data.filter(item => item.group === "edges").map(item => ({
    from: item.data.source, 
    to: item.data.target,
    weight: item.data.llr,
    label: item.data.action
  }));

  // const sortedEdges = edges.sort((a,b) => b.weight - a.weight)

  console.log("Nodes:")
  console.log(nodes)

  console.log("Edges:")
  console.log(edges)

  useEffect(() => {
    if (!graphRef.current) return;

    // create a new network
    const data = {
      nodes: new DataSet(nodes),
      edges: new DataSet(edges),
    };

    // Set options to render large datatset
    const options = {
      layout: {
        improvedLayout: false,
      },
    }
    const network = new Network(graphRef.current, data, options);

    return () => {
      network.destroy();
    };
  }, [nodes, edges]);

  return (
    <>
    <Heading size='md' style={{ textTransform: 'uppercase'}}>{title}</Heading>
    <Box mb={5}>
    <div ref={graphRef} style={{ height: '900px', width:'900px', maxWidth: '1400px', marginTop: '-20px' }}></div>
    </Box>
    </>
  );
};

export default PathsKG