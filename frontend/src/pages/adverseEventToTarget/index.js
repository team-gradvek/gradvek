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
          <title>Adverse Events to Target Results</title>
          <meta name="description" content="Gradvek Search Page" />
        </Head>
          <Box >
            <Heading size='md' mb={4} color="gray">Adverse Events to Target Results</Heading>
          <Card>
            <CardBody>
              <Stack spacing='3'>
                <Heading size='lg' color={theme.brand.blue}>Parkinson Disease</Heading>
                  <Divider />
                  <Heading size='sm'>Description</Heading>
                <Text>
                A progressive degenerative disorder of the central nervous system characterized by loss of dopamine producing neurons in the substantia nigra and the presence of Lewy bodies in the substantia nigra and locus coeruleus. Signs and symptoms include tremor which is most pronounced during rest, muscle rigidity, slowing of the voluntary movements, a tendency to fall back, and a mask-like facial expression.
                </Text>
                  <Divider />
                <Text color='gray' fontSize='sm'>
                EFO: MONDO_0005180| MeSH: D010300 | Orphanet: 319705 | UMLS: C0030567 | NCIt: C26845
                </Text>
              </Stack>
            </CardBody>
          </Card>
          </Box>
          <DataTable />
        </ResultsLayout>
        
 );
}