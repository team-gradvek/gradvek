import { Container, Box, Button, useColorMode } from '@chakra-ui/react'
import Footer from './footer'
import TopNav  from './topnav'

export default function Layout({ children }) {
  const { colorMode, toggleColorMode } = useColorMode();
    
    return   (
    <div>
      <TopNav />
      {/* <Container
           py={{
             base: '4',
             lg: '5',
           }}
           w='100%' maxWidth='1366px'
         > */}
      {children}
      {/* </Container> */}
      <Footer />
    </div>
    )
}