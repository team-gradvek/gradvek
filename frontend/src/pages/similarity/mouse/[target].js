import { useRouter } from 'next/router'
import DataTable from '@/components/results/DataTable'
import targetSimilarityMousePhenotype from '@/hooks/targetSimilarityMousePhenotypeHook';
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box } from '@chakra-ui/react';
import MouseTable from '@/components/similarity/MouseTable';

const columns = [
  {
    id: 1,
    name: 'Input'
  }, 
  {
    id: 2,
    name: 'Target'

  },
  {
    id: 3,
    name: 'Similarity Score'
  },
  {
    id: 4,
    name: 'Descriptor'
  },
]


const TargetSimilarityMousePhenotype = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

  const { data, isLoading, isError } = targetSimilarityMousePhenotype(target)

  if (isError) return <p>Failed to Load</p>

  if (isLoading) {
    return (
      <>
      <ResultsLayout>
      <Box p={5} w="100%">
        <DataTableSkeleton />
      </Box>
      </ResultsLayout>
      </>
    )
  }

  return (
    <>
    <ResultsLayout>
        <Head>
          <title>Target Similarity (Mouse Phenotype)</title>
        </Head>
      <Box p={5} w="100%">
      <MouseTable
          title={`Top 10 Targets Based on Similarity (Mouse Phenotype) for ${target}`}
          data={data}
          id={target} 
          columns={columns}
          />
          </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetSimilarityMousePhenotype