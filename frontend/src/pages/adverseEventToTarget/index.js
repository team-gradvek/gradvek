import { Box, Button, Tabs, TabList, TabPanels, Tab, TabPanel, Input } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../../components/layout'
import { Heading } from '@chakra-ui/react'



export default function AEIndex() {

 return (
      <Layout>
        <Head>
          <title>Adverse Event to Target</title>
          <meta name="description" content="Gradvek Search Page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Heading as='h1'>Adverse Event to Target</Heading>
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
      </Layout>
 );
}