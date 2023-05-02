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

  console.log(dataFromURL)
  const target = dataFromURL.target
  const ae = dataFromURL.ae

  const { data, isLoading, isError } = getPathwayData(`${encodeURIComponent(target)}/${encodeURIComponent(ae)}`)

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
          title={`Adverse Event Paths for ${target} and Adverse Event ID: ${ae}`}
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