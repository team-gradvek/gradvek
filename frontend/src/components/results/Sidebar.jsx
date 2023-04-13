import { Icon } from '@chakra-ui/icons'
import {
  Divider,
  Flex,
  Stack,
  Text,
} from '@chakra-ui/react'
import { Actions } from './filters/Actions'
import WeightSlider from './filters/Weights'

export const Sidebar = () => (
  <Flex as="section" minH="100vh" bg="bg-canvas">
    <Flex
      flex="1"
      bg="bg-surface"
      boxShadow="sm"
      maxW={{
        base: 'full',
        sm: 'xs',
      }}
      py={{
        base: '6',
        sm: '8',
      }}
      px={{
        base: '4',
        sm: '6',
      }}
    >
      <Stack justify="space-between" spacing="1">
        <Stack
          spacing={{
            base: '5',
            sm: '6',
          }}
          minW={200}
          paddingBottom={10}
          shouldWrapChildren
        >
          <Actions />
          <Divider />
          <WeightSlider />
        </Stack>
      </Stack>
    </Flex>
  </Flex>
)