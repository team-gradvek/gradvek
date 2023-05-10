import { useRouter } from 'next/router'
import targetSimilarityHook from '@/hooks/targetSimilarity';
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Heading, Text } from '@chakra-ui/react';
import averageSimilarityHook from '@/hooks/averageSimilarityHook';
import AverageSimilarityTable from '@/components/similarity/AverageSimilarityTable';

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
    name: 'Average'
  },
  {
    id: 4,
    name: 'Descriptors'
  },
]


const AverageSimilarityPathway = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

  const pageTitle = `Average Similarity Score for ${target}`

  const { data, isLoading, isError } = averageSimilarityHook(target)

  if (isError) {
    return (
      <>
       <ResultsLayout>
          <Box p={5} w="100%">
            <Heading size='md' mb={4}>Server Error</Heading>
            <Text size='md' mb={4}>Please try again later</Text>
          </Box>
        </ResultsLayout>
      </>
    )
  }

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
      <AverageSimilarityTable
          title={pageTitle}
          data={data}
          id={target} 
          columns={columns}
          />
          </Box>
    </ResultsLayout>
    </>
  )
}

export default AverageSimilarityPathway