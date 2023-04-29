import {
  Flex,
} from '@chakra-ui/react'
import Footer from '../footer';
import TopNav  from '../topnav'

function ResultsLayout({ children }) {
  
  return (
    <>
    <TopNav />
    <Flex
    as="section"
    direction={{
      base: 'column',
      lg: 'row',
    }}
    >
    {children}
    </Flex>
    <Footer />
    </>
    )
  }
  export default ResultsLayout;