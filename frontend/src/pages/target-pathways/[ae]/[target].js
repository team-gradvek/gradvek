import { useRouter } from 'next/router'
import PathTable from '@/components/results/PathTable'
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Card, CardBody, Text, Heading } from '@chakra-ui/react';
import getTargetPathwayData from '@/hooks/targetPathwayHook';


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query

  console.log(dataFromURL)
  const target = dataFromURL.target
  const ae = dataFromURL.ae

  const { data, isLoading, isError } = getTargetPathwayData(`${encodeURIComponent(ae)}/${encodeURIComponent(target)}`)

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
          <title>{`Targets Paths for ${ae} and Adverse Event ID: ${target}`}</title>
        </Head>
      <Box p={5} w="100%">
        <PathTable
          title={`Targets Paths for ${ae} and Adverse Event ID: ${target}`}
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