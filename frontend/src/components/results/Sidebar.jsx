import { Icon } from '@chakra-ui/icons'
import {
  Divider,
  Flex,
  Stack,
  Text,
} from '@chakra-ui/react'
import { Actions } from './filters/Actions'
import WeightSlider from './filters/Weights'
import theme from '@/styles/theme'

export const Sidebar = () => (
  <Flex as="section" minH="100vh">
    <Flex
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
          minW={250}
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