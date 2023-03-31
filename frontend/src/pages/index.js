import { Box, Button, Tabs, TabList, Card, TabPanels, Tab, TabPanel, Input, Container, Center, Text } from '@chakra-ui/react'
import Head from "next/head";
import Layout from '../components/layout'
import { Heading } from '@chakra-ui/react'



export default function Index() {

 return (
      <Layout>
        <Head>
          <title>Gradvek Search</title>
          <meta name="description" content="Gradvek Search Page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Box bg='#47819d'>
        <Container color='white' w='100%' maxWidth='1366px' py='10em' px='10em'>

        <Center>
          <Heading as='h1' m='1em' >Search</Heading>
        </Center>

        <Center>
         <Text fontSize='2xl'>An open source tool to designed to help scientists identify novel targets </Text>
        </Center>
        
        <Tabs isFitted variant='soft-rounded' colorScheme='blue' my='3em' size='lg'> 
          <Card p="4" m="4">
            <TabList>
              <Tab>Adverse Events</Tab>
              <Tab>Adverse Event to Target</Tab>
              <Tab>Target to Target</Tab>
            </TabList>
            </Card>
            <Card p="4" mx="4" mt="4">
            <TabPanels>
              <TabPanel>
              <Input variant='filled' placeholder='Search by target' size="lg"/>
              </TabPanel>
              <TabPanel>
              <Input variant='filled' placeholder='Search by adverse event' size="lg"/>
              </TabPanel>
              <TabPanel>
              <Input variant='filled' placeholder='Search by target' size="lg" />
              </TabPanel>
            </TabPanels>
            </Card>
        </Tabs>
        <Center>
          <Button size="lg" bg="#0F2A37" color="white">Search</Button>
        </Center>

        </Container>
        </Box>
      </Layout>
 );
}

