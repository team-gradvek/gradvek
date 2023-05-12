import { useRouter } from 'next/router'
import TargetTable from '@/components/results/TargetTable';
import getTargetData from '@/hooks/aeToTargetHook';
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Text, Heading } from '@chakra-ui/react';

const columns = [
  {
    id: 1,
    name: 'Symbol'
  }, 
  {
    id: 2,
    name: 'Name'

  },
  {
    id: 3,
    name: 'Type'
  },
  {
    id: 4,
    name: 'Weight'
  }, 
  {
    id: 5,
    name: 'Dataset'
  }
]


const AdverseEventToTarget = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const ae = dataFromURL.ae

  const title = `Targets for Adverse Event: ${ae}`

  const { data, isLoading, isError } = getTargetData(ae)

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
          <title>{title}</title>
        </Head>
      <Box p={5} w="100%">
        <TargetTable
          title={title}
          id={ae}
          columns={columns}
          data={data}
          />
      </Box>
    </ResultsLayout>
    </>
  )
}

export default AdverseEventToTarget