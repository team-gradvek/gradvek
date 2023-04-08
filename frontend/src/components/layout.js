import { Container, Box, Button, useColorMode } from '@chakra-ui/react'
import Footer from './footer'
import TopNav  from './topnav'

export default function Layout({ children }) {
  const { colorMode, toggleColorMode } = useColorMode();
    
    return   (
    <div>
      <TopNav />
      {children}
      <Footer />
    </div>
    )
}