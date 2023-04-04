import { Flex, Stack, Text } from '@chakra-ui/react'
import { NavButton } from './NavButton'
import {
  FiBarChart2,
  FiHome,
} from 'react-icons/fi'

function ResultsLayout({ children }) {
    
    return   (
      <Flex as="section" minH="100vh">
      <Flex
        flex="1"
        bg="bg-accent"
        maxW={{ base: 'full', sm: 'xs' }}
        py={{ base: '6', sm: '8' }}
        px={{ base: '4', sm: '6' }}
      >
        <Stack justify="space-between" spacing="1" width="full">
          <Stack spacing="8" shouldWrapChildren>
            {/* <Logo /> */}
            <Stack spacing="1">
            <Text fontSize="sm" color="on-accent-muted" fontWeight="medium">
                Descriptors
              </Text>
              <p>Gene</p>
              <p>Protein</p>
              <p>GWAS</p>
            </Stack>
            <Stack>
              <Text fontSize="sm" color="on-accent-muted" fontWeight="medium">
                Weights
              </Text>
              <Stack spacing="1">
                <p>Slider for Weights</p>
              </Stack>
            </Stack>
            <Stack>
              <Text fontSize="sm" color="on-accent-muted" fontWeight="medium">
                Receptor Types
              </Text>
              <Stack spacing="1">
               <p>Antagonist</p>
               <p>Inhibitor</p>
              </Stack>
            </Stack>
          </Stack>
        </Stack>
      </Flex>
      <Flex
        bg="#EBE9F1"
        maxW={{ base: 'full', sm: 'xs' }}
        py={{ base: '6', sm: '8' }}
        px={{ base: '4', sm: '6' }}
      >
      <Stack>
            {children}
          </Stack>
      </Flex>
    </Flex>
    )
}

export default ResultsLayout;