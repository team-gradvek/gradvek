import {
   Box,
   Button,
   ButtonGroup,
   Container,
   Flex,
   HStack,
   IconButton,
   useBreakpointValue,
   Heading
 } from '@chakra-ui/react'
 import { FiMenu } from 'react-icons/fi'
//  import logo  from '../gradvek-logo-32x32.png'
 import Image from 'next/image'
 import Link from 'next/link'
 
 export default function TopNav() {

   const isDesktop = useBreakpointValue({
     base: 'false',
     lg: true,

   })

   return ( 
     <Box as="section">
       <Box as="nav" bg="bg-surface" boxShadow="sm">
         <Container
           py={{
             base: '4',
             lg: '5',
           }}
           w='100%' maxWidth='1366px'
         >
           <HStack spacing="10" justify="space-between">
           <Link href="/">
            <Heading>Gradvek</Heading>
            </Link>
             {isDesktop ? (
               <Flex justify="right" flex="1">
                 <ButtonGroup variant="link" spacing="8">
                   {/* {['Search', 'API', 'Documentation'].map((item) => (
                     <Button key={item}>{item}</Button>
                   ))} */}
                  
                    <Button colorScheme='grey' variant="link" key="Search"><Link href='/'>Search </Link></Button>
                

                  
                    <Button colorScheme='grey' variant="link" key="API"><Link href='/'>API</Link></Button>
                

                 
                    <Button colorScheme='grey' variant="link" key="Documentation"><Link href='/'>Documentation</Link></Button>
                

                  
                    <Button colorScheme='grey' variant="solid" bg="#0F2A37" color="white">Sign in</Button>
                
                 </ButtonGroup>
               </Flex>
             ) : (
               <IconButton
                 variant="ghost"
                 icon={<FiMenu fontSize="1.25rem" />}
                 aria-label="Open Menu"
               />
             )}
           </HStack>
         </Container>
       </Box>
     </Box>
   )
 }