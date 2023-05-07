import ResultsLayout from '@/components/results/ResultsLayout';
import Head from "next/head";
import { Box, Button, Heading, Card, CardBody, Text, Container } from '@chakra-ui/react';
import Uploader from '@/hooks/dropzoneUploader';



const Uploads = () => {

  return (
    <>
    <ResultsLayout>
        <Head>
          <title>Data Uploads</title>
        </Head>
      <Container w='100%' maxWidth='1366px'>
          <Box my={5}>
            <Heading size='lg' mb={4}>Data Uploads</Heading>
            <Text size='md' mb={4}>Upload Custom Data Sets</Text>
            <Uploader />
          </Box>
        </Container>
    </ResultsLayout>
    </>
  )
}

export default Uploads