import {
  Flex,
} from '@chakra-ui/react'
import TopNav  from '../TopNav'

function TargetToTargetResultsLayout({ children }) {

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
export default TargetToTargetResultsLayout;