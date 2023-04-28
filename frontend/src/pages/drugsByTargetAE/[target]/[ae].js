import { useRouter } from 'next/router'
// import DataTable from '@/components/results/DataTable'
// import getAdverseEvent from "../../hooks/targetToAdverseEventHook"
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Heading } from '@chakra-ui/react';
import DrugsTable from '@/components/drugs/DrugsTable';
import getDrugsByTargetAE from '@/hooks/drugsByTargetAEHook';

const columns = [
  {
    id: 1,
    name: 'Drug ID'
  }, 
  {
    id: 2,
    name: 'Name'

  },
  {
    id: 3,
    name: 'Weights'
  },
]


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target
  const ae = dataFromURL.ae

  console.log(dataFromURL)

  const { data, isLoading, isError } = getDrugsByTargetAE(target, ae)

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
          <title>Drugs by Target and Adverse Event</title>
        </Head>
      <Box p={5} w="100%">
      <DrugsTable
          title={`Available Drugs for Target: ${target} with Adverse Event ID: ${ae}`}
          data={data}
          columns={columns}
          />
          </Box>
    </ResultsLayout>
    </>
  )
}

export default TargetToAdverseEvents