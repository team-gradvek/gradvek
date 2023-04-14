import {
  Flex,
  Stack,
  Box,
} from '@chakra-ui/react'
import { Sidebar } from './Sidebar'
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
      {/* <TargetToTargetSidebar />
      <Box p={5} w="100%" bg="#eee">
        <Stack
          spacing={{
            base: '8',
            lg: '6',
          }}
        >
          {children}
        </Stack>
      </Box> */}
    </Flex>
    </>
  )
}
export default TargetToTargetResultsLayout;