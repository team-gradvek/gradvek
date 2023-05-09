import {
  Avatar,
  Box,
  Checkbox,
  HStack,
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
import 'react-loading-skeleton/dist/skeleton.css'
import DataTableSkeleton from './DataTableSkeleton'



const TargetTable = ({title, columns, data, isError, isLoading}) => {

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
  

  if (isError) {
    return (
      <>
        <Card>
          <CardBody>
            <Heading size='md' mb={4}>{title}</Heading>
            <Text size='md' mb={4}>An Error Occurred. Please try again.</Text>
          </CardBody>
        </Card>
      </>
    )
  }

  if (isLoading) {
    return (
      <>
      <Box p={5} w="100%">
        <DataTableSkeleton />
      </Box>
      </>
    )
  }

  return (
  <>
  <Heading size='md' mb={4}>{title}</Heading>
  <Table bg="white" borderRadius={5}>
    <Thead>
      <Tr>
      {columns.map((col) => (
        <Th key={col.id}>{col.name}</Th>
      ))}
      </Tr>
    </Thead>
    <Tbody>
      {data.map((item) => (
        <Tr key={item.id}>
          <Td>
            <HStack>
            <Avatar name={item.symbol} boxSize="10" />
            <Text className="capitalize" fontWeight="medium">{item.symbol}</Text>
            </HStack>
          </Td>
          <Td>
              <Text className="capitalize" fontWeight="medium">{item.name}</Text>
          </Td>
          <Td>
           <Text color="muted">{item.type}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.llr.toFixed(2)}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.dataset}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default TargetTable