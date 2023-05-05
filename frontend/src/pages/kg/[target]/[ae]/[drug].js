import { useRouter } from 'next/router'
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Text, Heading } from '@chakra-ui/react';
import getPathwayData from '@/hooks/pathwaysHook'
import PathsKG from '@/components/graph/PathsKG';


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query

  console.log(dataFromURL)
  const target = dataFromURL.target
  const ae = dataFromURL.ae
  const drug = dataFromURL.drug

  const pageTitle = `Knowledge Graph for ${target} with Adverse Event ID: ${ae} and Drug ID: ${drug}`

  const { data, isLoading, isError } = getPathwayData(`${target}/${ae}/${drug}`)

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

export default TargetToAdverseEvents