import { Box, Card, CardBody, Stack, Divider, Text, Flex } from '@chakra-ui/react'
import Head from "next/head";
import { Heading } from '@chakra-ui/react'
import DataTable from '@/components/results/DataTable'
import theme from '@/styles/theme';
import { ResultsSidebar } from '@/components/results/ResultsSidebar';
import { Descriptors } from '@/components/results/filters/Descriptors';
import { Actions } from '@/components/results/filters/Actions';
import { WeightSlider } from '@/components/results/filters/WeightSlider';
import { actionsData } from '@/components/data/FetchActionsData';
import ResultsLayout from '@/components/results/ResultsLayout';

// Placeholder data
import { events } from '@/components/data/FetchAdverseEventData';

const checkboxData = [
  {
    name: 'Gene',
  },
  {
    name: 'Protein'
  },
  {
    name: 'GWAS'
  },
  {
    name: 'Phenotype'
  },
  {
    name: 'Reactome'
  },
  {
    name: 'Signor'
  },
  {
    name: 'IntAct'    
  }
]


export default function TargetToTargetResults() {
 return (
      <ResultsLayout>
        <Head>
          <title>Target to Target Results</title>
        </Head>

        <Box display='flex' w="100%">
      
      {/* Sidebar */}
        <Box w="25%" minW='250px'>
          <ResultsSidebar>
            <Divider />
            <Descriptors 
              title = 'Descriptors'
              checkboxArray = {checkboxData} />
            <Divider />
            <Actions 
              title = 'Actions'
              checkboxArray = {actionsData} />
            <Divider />
            <WeightSlider
              title='Adverse Event Name'
              range={{min: '0', mid: '50', max: '100'}} 
              initial={{ min: '25', max: '75'}}/>
          </ResultsSidebar>
        </Box>
        <Box p={5} w="75%" bg="#eee">

          {/* Page Heading */}
          <Heading size='md' mb={4}>Target to Target Results</Heading>
          {/* Search Input Display */}
          <Box display='flex' alignItems='center' justifyContent='space-between' mb='5'>
            <Box w="50%" bg="#eee">  
            <Card>
              <CardBody>
                <Stack spacing='3'>
                  <Heading size='lg' color={theme.brand.color}>Input: DRD3</Heading>
                    <Divider />
                    <Heading size='sm'>Description</Heading>
                  <Text>
                  Dopamine receptor whose activity is mediated by G proteins which inhibit adenylyl cyclase. Promotes cell proliferation.
                  </Text>
                    <Divider />
                  <Text color='gray' fontSize='sm'>
                  ID: 10029282
                  </Text>
                </Stack>
              </CardBody>
            </Card>
            </Box>
          </Box>
          {/* Results Table */}
          <Box w='100%' mb='5'>
          <Heading size='md' mb={4}>Top 10 Target Similarity Results</Heading>
          <DataTable
          title="Targets from Adverse Event" 
          />
          </Box>
        </Box>

        </Box>

      </ResultsLayout>
 );
}