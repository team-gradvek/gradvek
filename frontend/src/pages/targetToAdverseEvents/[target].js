import { useRouter } from 'next/router'
import DataTable from '@/components/results/DataTable'
import getAdverseEvent from "../../hooks/targetToAdverseEventHook"
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Card, CardBody, Text, Heading } from '@chakra-ui/react';
import getPathwayData from '@/hooks/pathwaysHook'

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


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

  const { adverseEvent, isLoading, isError } = getAdverseEvent(target)
  const { data, isLoading: isLoadingPath, isError:isErrorPath } = getPathwayData(target)

  const title = `Adverse Events for ${target}`

  if (isError || isErrorPath) {
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

  if (isLoading || isLoadingPath) {
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
          <title>{title}</title>
        </Head>
      <Box p={5} w="100%">
        <DataTable
          title={title}
          id={target} 
          target={target}
          columns={columns}
          data={adverseEvent}
          />
      </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetToAdverseEvents