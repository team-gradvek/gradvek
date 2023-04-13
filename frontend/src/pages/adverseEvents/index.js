import { Box, Card, CardBody, Stack, Divider, Text, Flex } from '@chakra-ui/react'
import Head from "next/head";
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/ResultsLayout';
import DataTable from '@/components/results/DataTable'
import theme from '@/styles/theme';


export default function TargetToAEResults() {
 return (
      <ResultsLayout>
        <Head>
          <title>Target to Adverse Events Results</title>
          <meta name="description" content="Gradvek Search Page" />
        </Head>
          <Box >
            <Heading size='md' mb={4} color="gray">Target to Adverse Events</Heading>
          <Card>
            <CardBody>
              <Stack spacing='3'>
                <Heading size='lg' color={theme.brand.blue}>DRD3</Heading>
                  <Divider />
                  <Heading size='sm' >Description</Heading>
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
          <DataTable />
        </ResultsLayout>
 );
}