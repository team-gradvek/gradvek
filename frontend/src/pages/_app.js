// pages/_app.js
import '@/styles/globals.css'
import { ChakraProvider, extendTheme } from '@chakra-ui/react'

const config = {
  initialColorMode: 'dark'
}

const theme = extendTheme({config})



function App({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default App
