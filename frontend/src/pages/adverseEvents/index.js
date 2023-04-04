import { Box, Button, Tabs, TabList, TabPanels, Tab, TabPanel, Input } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../../components/layout'
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/layout';



export default function TargetToAEResults() {

 return (
      <Layout>
        <Head>
          <title>Target to Adverse Events Results</title>
          <meta name="description" content="Gradvek Search Page" />
        </Head>
        <ResultsLayout>
          <Heading as='h1'>Target to Adverse Events Results</Heading>
        </ResultsLayout>
      </Layout>
 );
}