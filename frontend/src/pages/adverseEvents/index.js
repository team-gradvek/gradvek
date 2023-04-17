import { Box, Card, CardBody, Stack, Divider, Text, Flex } from '@chakra-ui/react'
import Head from "next/head";
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/ResultsLayout';
import DataTable from '@/components/results/DataTable'
import theme from '@/styles/theme';
import { Actions } from '@/components/results/filters/Actions';
import { WeightSlider } from '@/components/results/filters/WeightSlider';
import { Descriptors } from '@/components/results/filters/Descriptors';
import { actionsData } from '@/components/data/FetchActionsData';

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


export default function TargetToAEResults() {
 return (
      <ResultsLayout>
        <Head>
          <title>Target to Adverse Events Results</title>
        </Head>
        <Box display='flex' w="100%">
      

        {/* Results Page Filters */}
        <Box w="25%" minW='250px'>
          <Stack spacing={[4]} direction={['column']} p='5'>
            <Heading fontSize='xl'>Filters</Heading>
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
          </Stack>
        </Box>
        <Box p={5} w="75%" bg="#eee">
          {/* Result Page Heading */}
          <Heading size='md' mb={4}>Target to Adverse Event Results</Heading>
          {/* Results Input Display */}
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
          <Heading size='md' mb={4}>Adverse Events Associated with Target</Heading>
          <DataTable/>
          </Box>
        </Box>

        </Box>
        </ResultsLayout>
 );
}