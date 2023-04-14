import {
  Flex,
} from '@chakra-ui/react'
import TopNav  from '../TopNav'

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
    </>
    )
  }
  export default ResultsLayout;