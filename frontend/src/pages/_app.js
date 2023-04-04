// pages/_app.js
import '@/styles/globals.css'
import { ChakraProvider, Heading, Text } from '@chakra-ui/react'
import theme from '../styles/theme'


function App({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default App
