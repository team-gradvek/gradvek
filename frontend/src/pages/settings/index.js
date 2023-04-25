import getSettings from '../../hooks/getSettingsHook'
import DataTableSkeleton from '@/components/results/DataTableSkeleton'
import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Divider, Flex, Grid, Heading } from '@chakra-ui/react';
import DatasetsTable from '@/components/settings/DatasetsTable';
import SystemDataTable from '@/components/settings/SystemDataTable';
import DescriptorsTable from '@/components/settings/DescriptorsTable';
import ActionsTable from '@/components/settings/ActionsTable';



const descriptorCols = [
  {
  id: 1,
  name: 'Descriptor'
  }
]

const actionsCols = [
  {
  id: 1,
  name: 'Action'
  }, 
  {
  id: 2,
  name: 'Total'
  }, 

]

const datasetCols = [
  {
    id: 1,
    name: 'Datasets'
  }, 
]

const systemDataCols = [
  {
    id: 1,
    name: 'Type'
  }, 
  {
    id: 2,
    name: 'Count'
  }, 
]


const Settings = () => {

  // Configure API paths to retrieve data
  const descriptors = 'api/descriptors'
  const actionsWithCount = 'api/actions'
  const datasets = 'api/datasets'
  const systemDataWithCounts = 'api/count'



  // Unpack all objects and assign a new variable name to use multiple SWRs
  // Get settings via Hook
  const { data: descriptorsData, isLoading: isLoadingDescriptors, isError: isErrorDescriptors } = getSettings(descriptors)

  // Get settings via Hook
  const { data: actionsData, isLoading: isLoadingActions, isError: isErrorActions } = getSettings(actionsWithCount)

  // Get settings via Hook
  const { data: datasetsData,  isLoading:isLoadingDatasets, isError: isErrorDatasets } = getSettings(datasets)

  // Get settings via Hook
  const { data: systemData, isLoading: isLoadingSystem, isError: isErrorSystem } = getSettings(systemDataWithCounts)

  if (isErrorDescriptors || isErrorActions || isErrorDatasets || isErrorSystem ) return <p>Failed to Load</p>

  if (isLoadingDescriptors || isLoadingActions || isLoadingDatasets || isLoadingSystem) {
    return (
      <>
      <ResultsLayout>
      <Box p={5} w="25%">
        <DataTableSkeleton />
      </Box>
      <Box p={5} w="25%">
        <DataTableSkeleton />
      </Box>
      <Box p={5} w="25%">
        <DataTableSkeleton />
      </Box>
      <Box p={5} w="25%">
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
          <title>Application Settings & Data</title>
        </Head>
      {/* Grid for small, med, large, xl screens */}
      {/* <Heading>
        Application Settings & Data
      </Heading>
      <Divider /> */}

      <Box w="100%" m={2}>
      <Box m={3}>
        <DatasetsTable
            title="Datasets in System"
            data={datasetsData}
            columns={datasetCols}
            />
        </Box>
        <Box m={3}>
        <SystemDataTable
            title="Database Counts by Type"
            data={systemData}
            columns={systemDataCols}
            />
        </Box>
      </Box>

      <Box w="100%" m={2}>
      <Box m={3}>
        <ActionsTable
            title="Total Actions"
            data={actionsData}
            columns={actionsCols}
            />
      </Box>
      {/* <Box m={3}>
        <DescriptorsTable
            title="Descriptors Available"
            data={descriptorsData}
            columns={descriptorCols}
            />
        </Box>
        */}
      </Box>

    </ResultsLayout>
    </>
  )
}

export default Settings