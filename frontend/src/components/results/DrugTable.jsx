import {
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from '@chakra-ui/react'


const DrugTable = ({ title, columns, data}) => {
  return (
  <>
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
        <Tr key={item.drugId}>
          <Td>
            <Text fontWeight="bold">{item.drugName}</Text>
          </Td>
          <Td>
            <Text>{item.drugId}</Text>
          </Td>
          <Td>
            <Text>{item.weight}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default DrugTable