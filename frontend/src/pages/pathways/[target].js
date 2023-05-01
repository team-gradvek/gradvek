import { useRouter } from 'next/router'
import PathTable from '@/components/results/PathTable'
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Card, CardBody, Text, Heading } from '@chakra-ui/react';
import getPathwayData from '@/hooks/pathwaysHook'


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

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
          <title>Target to Adverse Events Path</title>
        </Head>
      <Box p={5} w="100%">
        <PathTable
          title={`Adverse Event Paths for ${target}`}
          data={data}
          isLoading={isLoading}
          isError={isError}
          />
      </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetToAdverseEvents