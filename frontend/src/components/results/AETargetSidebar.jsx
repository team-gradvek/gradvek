import { Icon } from '@chakra-ui/icons'
import {
  Divider,
  Heading,
  Stack,
} from '@chakra-ui/react'
import { Actions } from './filters/Actions'
import WeightSlider from './filters/Weights'
import { Descriptors } from './filters/Descriptors'

export const AETargetSidebar = () => (
  <Stack spacing={[4]} direction={['column']} p='5'>
    <Heading fontSize='xl'>Filters</Heading>
    <Divider />
    <Descriptors />
    <Divider />
    <Actions />
    <Divider />
    <WeightSlider />
    <Divider />
  </Stack>
  )