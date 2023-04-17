import { Heading, Link } from '@chakra-ui/react'
import theme from '@/styles/theme'

export const Logo = ({brand}) => (
  <Link href="/">
    <Heading color={theme.brand.color}>{brand}</Heading>
  </Link>
)