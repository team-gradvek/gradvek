import { Box, Button, Tabs, TabList, TabPanels, Tab, TabPanel, Input } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../../components/layout'
import { Heading } from '@chakra-ui/react'
import ResultsLayout from '@/components/results/layout';



export default function AEIndex() {

 return (
      <ResultsLayout>
        <Head>
          <title>Adverse Events Results</title>
          <meta name="description" content="Gradvek Search Page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Heading as='h1'>Adverse Events Results</Heading>
        <Tabs variant='soft-rounded' colorScheme='green'>
            <TabList>
              <Tab>Adverse Events</Tab>
              <Tab>Adverse Event to Target</Tab>
              <Tab>Target to Target</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
              <Input placeholder='Adverse Events' />
              </TabPanel>
              <TabPanel>
              <Input placeholder='Adverse Event to Target' />
              </TabPanel>
              <TabPanel>
              <Input placeholder='Target to Target' />
              </TabPanel>
            </TabPanels>
        </Tabs>
      </ResultsLayout>
 );
}