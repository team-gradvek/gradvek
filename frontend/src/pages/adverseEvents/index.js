import { Box, Card, CardBody, Stack, Divider, Text, Flex } from '@chakra-ui/react'
import Head from "next/head";
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/ResultsLayout';
import DataTable from '@/components/results/DataTable'
import theme from '@/styles/theme';
import { AETargetSidebar } from '@/components/results/AETargetSidebar';


export default function TargetToAEResults() {
 return (
      <ResultsLayout>
        <Head>
          <title>Target to Adverse Events Results</title>
        </Head>
        <Box display='flex' w="100%">
      
        <Box w="25%" minW='250px'>
          <AETargetSidebar />
        </Box>
        <Box p={5} w="75%" bg="#eee">

          {/* Search Page Heading */}
          <Heading size='md' mb={4}>Target to Adverse Event Results</Heading>
          {/* Search Input Display */}
          <Box display='flex' alignItems='center' justifyContent='space-between' mb='5'>
            <Box w="50%" bg="#eee">  
            <Card>
              <CardBody>
                <Stack spacing='3'>
                  <Heading size='lg' color={theme.brand.blue}>Input: DRD3</Heading>
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
          {/* Search Results Table */}
          <Box w='100%' mb='5'>
          <Heading size='md' mb={4}>Adverse Events Associated with Target</Heading>
          <DataTable/>
          </Box>
        </Box>

        </Box>
        </ResultsLayout>
 );
}