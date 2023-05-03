import {
  Button,
  Container,
  Divider,
  Stack,
  Text,
  useColorMode,
  Icon
} from '@chakra-ui/react'
import Link from 'next/link';
import { AiOutlineArrowRight } from 'react-icons/ai';

export default function Footer() {

  // const { colorMode, toggleColorMode } = useColorMode();

 return (
  <Container as="footer" role="contentinfo" w='100%' maxWidth='1366px'>
    <Divider />
    <Stack
      py={{
        base: '12',
        md: '16',
      }}
    >   
        <Stack direction="row" spacing="8">
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              Data & Settings
            </Text>
            <Stack spacing="4" shouldWrapChildren>
              <Button variant="link"><Link href='/settings'>Settings</Link></Button>
              <Button variant="link"><Link href='/settings/uploads'>Data Upload</Link></Button>
              <Button variant="link"><Link href='https://github.com/team-gradvek/gradvek'>Documentation</Link></Button>
              <Button variant="link"><Link href='https://platform.opentargets.org/downloads'>Open Target</Link></Button>
              <Button variant="link">API Docs</Button>
            </Stack>
          </Stack>
          
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              Sample Pathways
            </Text>
            <Stack spacing="3" shouldWrapChildren>
              <Button variant="link"><Link href='/pathways/drd3'>Target</Link></Button>
              <Button variant="link"><Link href='/pathways/drd3/parkisonism'>Target + AE</Link></Button>
              <Button variant="link"><Link href='/pathways/drd3/LEVODOPA'>Target + AE + Drug</Link></Button>
              <Divider />
              <Button variant="link"><Link href='/target-pathways/parkisonism'>Adverse Event</Link></Button>
              <Button variant="link"><Link href='/target-pathways/parkisonism/drd3'>AE + Target</Link></Button>
              <Button variant="link"><Link href='/target-pathways/parkisonism/drd3/LEVODOPA'>AE + Target + Drug</Link></Button>
            </Stack>
          </Stack>
          <Stack spacing="4" minW="36" flex="1">
            <Text fontSize="sm" fontWeight="semibold" color="subtle">
              Sample Knowledge Graphs
            </Text>
            <Stack spacing="3" shouldWrapChildren>
              <Button variant="link"><Link href='/kg/DRD3'>Target KG</Link></Button>
              <Button variant="link"><Link href='/kg/DRD3/extrapyramidal%20disorder'>Target with AE KG</Link></Button>
              <Button variant="link"><Link href='/kg/DRD3/extrapyramidal%20disorder/LEVODOPA'>Target with AE and Drug KG</Link></Button>
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