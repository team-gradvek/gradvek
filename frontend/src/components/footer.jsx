import {
  Button,
  Container,
  Divider,
  Stack,
  Text,
  useColorMode
} from '@chakra-ui/react'

export default function Footer() {

  // const { colorMode, toggleColorMode } = useColorMode();

 return (
  <Container as="footer" role="contentinfo" w='100%' maxWidth='1366px'>
    <Stack
      py={{
        base: '12',
        md: '16',
      }}
    >   
        <Stack direction="row" spacing="8">
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              Product
            </Text>
            <Stack spacing="4" shouldWrapChildren>
              <Button variant="link">Features</Button>
              <Button variant="link">Documentation</Button>
              <Button variant="link">Data Management</Button>
              <Button variant="link">API Docs</Button>
            </Stack>
          </Stack>
          
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              About
            </Text>
            <Stack spacing="3" shouldWrapChildren>
              <Button variant="link">Contact</Button>
              <Button variant="link">Team</Button>
              <Button variant="link">License</Button>
            </Stack>
          </Stack>
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              Resources
            </Text>
            <Stack spacing="3" shouldWrapChildren>
              <Button variant="link">Open Target</Button>
              <Button variant="link">Community</Button>
            </Stack>
          </Stack>
          
        </Stack>
  
    </Stack>
    <Divider />
    <Stack
      pt="8"
      pb="12"
      justify="space-between"
      direction={{
        base: 'column-reverse',
        md: 'row',
      }}
      align="center"
    >
      <Text fontSize="sm" color="subtle">
        &copy; {new Date().getFullYear()} Gravek 2.0
      </Text>
    </Stack>
  </Container>



 );
}