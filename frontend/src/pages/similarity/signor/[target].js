import { useRouter } from 'next/router'
import targetSimilarityHook from '@/hooks/targetSimilarity';
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Heading, Text } from '@chakra-ui/react';
import SimilarityTable from '@/components/similarity/SimilarityTable';

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


const TargetSimilarityPathway = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target
  const descriptor = "Signor"

  const pageTitle = `Targets Based on Similarity: ${descriptor} for ${target}`

  const { data, isLoading, isError } = targetSimilarityHook("signor", target)

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
          <title>{pageTitle}</title>
        </Head>
      <Box p={5} w="100%">
      <SimilarityTable
          title={pageTitle}
          data={data}
          id={target} 
          columns={columns}
          descriptor={descriptor}
          />
          </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetSimilarityPathway