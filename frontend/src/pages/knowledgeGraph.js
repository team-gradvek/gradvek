import { useState, useEffect } from 'react';
import PathKG from '@/components/graph/PathsKG';
import getPathwayData from '@/hooks/pathwaysHook'

function KnowledgeGraph() {

   // Get data from URL
  const target = "DRD3"

  const { data, isLoading, isError } = getPathwayData(target)

  // Render the query results once they're available
  return (
     <PathKG
      title="Knowledge Graph"
      target={target}
      data={data}
        />
  );
}

export default KnowledgeGraph;