import {
   Box,
   Button,
   ButtonGroup,
   Container,
   Flex,
   HStack,
   Heading
 } from '@chakra-ui/react'
 import Link from 'next/link'
 import theme from '@/styles/theme'
 
 export default function TopNav() {
   return ( 
     <Box as="section">
       <Box as="nav" bg="bg-surface" boxShadow="sm">
         <Container
           py={{
             base: '4',
             lg: '5',
           }}
           w='100%' maxW='1480px'
         >
           <HStack spacing="10" justify="space-between">
           <Link href="/">
            <Heading color={theme.brand.color}>Gradvek</Heading>
            </Link>
               <Flex justify="right" flex="1">
                 <ButtonGroup variant="link" spacing="8">
                  
                    <Button colorScheme='grey' variant="link" key="Search"><Link href='/'>Search </Link></Button>
                            
                    <Button colorScheme='grey' variant="link" key="Settings"><Link href='/settings'>Settings</Link></Button>
                 
                    <Button colorScheme='grey' variant="link" key="Documentation"><Link href='https://github.com/team-gradvek/gradvek'>Documentation</Link></Button>
                
                 </ButtonGroup>
               </Flex>
           </HStack>
         </Container>
       </Box>
     </Box>
   )
 }