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
  Button,
} from '@chakra-ui/react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'


const DataTableSkeleton = () => {

  return (
  <>
  <Heading size='md' mb={4}>{<Skeleton />}</Heading>
  <Table bg="white" borderRadius={5}>
    <Thead>
      <Tr>
        <Th>{<Skeleton />}</Th>
        <Th>{<Skeleton />}</Th>
        <Th>{<Skeleton />}</Th>
        <Th>{<Skeleton />}</Th>
      </Tr>
    </Thead>
    <Tbody>
        <Tr>
          <Td>
            <Text>{<Skeleton />}</Text>
          </Td>
          <Td>
            <Text color="muted">{<Skeleton />}</Text>
          </Td>
          <Td>
            <Text color="muted">{<Skeleton />}</Text>
          </Td>
          <Td>
            <Text color="muted">{<Skeleton />}</Text>
          </Td>
        </Tr>
    </Tbody>
  </Table>
  </>
  )
}

export default DataTableSkeleton