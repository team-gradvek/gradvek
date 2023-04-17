import { Heading, Stack } from '@chakra-ui/react'
// import { Logo } from './Logo'

export const ResultsSidebar = ({ children }) => (
  <>
  <Stack spacing={[4]} direction={['column']} p='5'>
    {/* <Logo brand='Gradvek' /> */}
    <Heading fontSize='xl'>Filters</Heading>
    {children}
  </Stack>
  </>
  )