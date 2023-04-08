import { Box, Button, Tabs, TabList, TabPanels, Tab, TabPanel, Input } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../../components/layout'
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/layout';



export default function AEToTargetResults() {

 return (
      <Layout>
        <Head>
          <title>Adverse Events to Target Results</title>
          <meta name="description" content="Gradvek Search Page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <ResultsLayout>
          <Heading as='h1'>Adverse Events to Target Results</Heading>
        </ResultsLayout>
      </Layout>
 );
}