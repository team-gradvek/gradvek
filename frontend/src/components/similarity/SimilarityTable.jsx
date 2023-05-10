import {
  Heading,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  Card, CardBody, 
} from '@chakra-ui/react'
import Link from 'next/link'
import 'react-loading-skeleton/dist/skeleton.css'
import theme from '@/styles/theme'


const SimilarityTable = ({data, title, columns, descriptor}) => {

  if (data.length == 0) {
    return (
      <>
        <Card>
          <CardBody>
            <Heading size='md' mb={4}>{title}</Heading>
            <Text size='md' mb={4}>No Data Available</Text>
          </CardBody>
        </Card>
      </>
    )
  }

  return (
  <>
  <Heading className="uppercase" size='md' mb={4}>{title}</Heading>
  <Table bg="white" borderRadius={5}>
    <Thead>
      <Tr>
      {columns.map((col) => (
        <Th key={col.id}>{col.name}</Th>
      ))}
      </Tr>
    </Thead>
    <Tbody>
      {data.map((item, index) => (
        <Tr key={item.id || index}>
          <Td>
            <Text className="capitalize" fontWeight="medium" color={theme.brand.color}><Link href={{ pathname: `/targetToAdverseEvents/` + item.target1 }}>{item.target1}</Link></Text>
          </Td>
          <Td>
            <Text className="capitalize" fontWeight="medium" color={theme.brand.color}>
              <Link href={{ pathname: `/targetToAdverseEvents/` + item.target2 }}>{item.target2}</Link>
              </Text>
          </Td>
          <Td>
           <Text color="muted">{item.similarity.toFixed(2)}</Text>
          </Td>
          <Td>
           <Text color="muted">{descriptor}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default SimilarityTable