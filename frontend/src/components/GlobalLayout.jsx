import { useColorMode } from '@chakra-ui/react'
import Footer from './Footer'
import TopNav  from './TopNav'

export default function Layout({ children }) {    
    return   (
    <div>
      <TopNav />
      {children}
      <Footer />
    </div>
    )
}