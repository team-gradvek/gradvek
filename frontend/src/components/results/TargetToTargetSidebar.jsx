import { Icon } from '@chakra-ui/icons'
import {
  Divider,
  Box, Stack, Text, Heading
} from '@chakra-ui/react'
import { Actions } from './filters/Actions'
import { Descriptors } from './filters/Descriptors'
import WeightSlider from './filters/Weights'

export const TargetToTargetSidebar = () => (
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