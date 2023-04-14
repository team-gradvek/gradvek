import { Box, Button, Tabs, TabList, Card, TabPanels, Tab, TabPanel, Input, Container, Center, Text } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../components/GlobalLayout'
import { Heading } from '@chakra-ui/react'
import TargetToAESearch from '@/components/search/targetToAdverseEventSearch';
import AdverseEventToTargetSearch from '@/components/search/adverseEventToTarget';
import TargetToTargetSimilaritySearch from '@/components/search/targetToTargetSimilaritySearch';
import Link from 'next/link'
import theme from '@/styles/theme';


export default function Index() {

 return (
      <Layout>
        <Head>
          <title>Gradvek Search</title>
          <meta name="description" content="Gradvek Search Page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Box bg={theme.brand.color}>
        <Container color='white' w='100%' maxWidth='1366px' py='10' px='10em'>

        <Center>
          <Heading as='h1' m='1em' >Search</Heading>
        </Center>

        <Center>
         <Text fontSize='2xl'>An open source tool designed to identify novel targets and adverse events in drug research </Text>
        </Center>
        
        <Tabs isFitted variant='soft-rounded' colorScheme='blue' my='3em' size='lg'> 
          <Card p="4" m="4">
            <TabList>
              <Tab>Target to Adverse Event</Tab>
              <Tab>Adverse Event to Target</Tab>
              <Tab>Target to Target</Tab>
            </TabList>
            </Card>
            <Card p="4" mx="4" mt="4">
            <TabPanels>
              <TargetToAESearch />
              <AdverseEventToTargetSearch />
              <TargetToTargetSimilaritySearch />
            </TabPanels>
            </Card>
        </Tabs>
        </Container>
        </Box>
      </Layout>
 );
}

