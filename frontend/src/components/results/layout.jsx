import { Container, Box, Button, useColorMode } from '@chakra-ui/react'

function ResultsLayout({ children }) {
    
    return   (
    <Container my="3">
      {children}
    </Container>
    )
}

export default ResultsLayout;