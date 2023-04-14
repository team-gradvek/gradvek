import { Box, Card, CardBody, Stack, Divider, Text, Flex } from '@chakra-ui/react'
import Head from "next/head";
import { Heading } from '@chakra-ui/react'
import TargetToTargetResultsLayout from '@/components/results/TargetToTargetResultsLayout';
import DataTable from '@/components/results/DataTable'
import theme from '@/styles/theme';
import { TargetToTargetSidebar } from '@/components/results/TargetToTargetSidebar';

export default function TargetToTargetResults() {
 return (
      <TargetToTargetResultsLayout>
        <Head>
          <title>Target to Target Results</title>
        </Head>

        <Box display='flex' w="100%">
      
        <Box w="25%" minW='250px'>
          <TargetToTargetSidebar />
        </Box>
        <Box p={5} w="75%" bg="#eee">

          {/* Search Page Heading */}
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
          {/* Search Results Table */}
          <Box w='100%' mb='5'>
          <Heading size='md' mb={4}>Top 10 Target Similarity Results</Heading>
          <DataTable/>
          </Box>
        </Box>

        </Box>

      </TargetToTargetResultsLayout>
 );
}