import { useColorMode } from '@chakra-ui/react'
import Footer from './footer'
import TopNav  from './topnav'

export default function Layout({ children }) {    
    return   (
    <div>
      <TopNav />
      {children}
      <Footer />
    </div>
    )
}