import { useRouter } from 'next/router'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Text, Heading } from '@chakra-ui/react';
import Skeleton from 'react-loading-skeleton';
import getPathwayData from '@/hooks/pathwaysHook'
import PathsKG from '@/components/graph/PathsKG';

const columns = [
  {
    id: 1,
    name: 'Adverse Event'
  }, 
  {
    id: 2,
    name: 'ID'

  },
  {
    id: 3,
    name: 'Weights'
  },
  {
    id: 4,
    name: 'Dataset'
  }
]


const TargetToAdverseEventsKG = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

  const pageTitle = `Adverse Event Paths for ${target}`

  const { data, isLoading, isError } = getPathwayData(target)

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
        <Skeleton />
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
          <PathsKG
          title={pageTitle}
          target={target}
          data={data}
           />
      </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetToAdverseEventsKG