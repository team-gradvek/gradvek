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
  Card, CardBody, Divider, 
} from '@chakra-ui/react'
import 'react-loading-skeleton/dist/skeleton.css'
import DataTableSkeleton from './DataTableSkeleton'

const nodeCols = [
  {
    id: 1,
    name: 'id'
  }, 
  {
    id: 2,
    name: 'group'

  },
  {
    id: 3,
    name: 'name'
  },
  {
    id: 4,
    name: 'class'
  }
]

const edgeCols = [
  {
    id: 1,
    name: 'id'
  }, 
  {
    id: 2,
    name: 'group'

  },
  {
    id: 3,
    name: 'weight'
  },
  {
    id: 4,
    name: 'from'
  },
  {
    id: 5,
    name: 'action'
  },
  {
    id: 6,
    name: 'to'
  }
]


const PathTable = ({title, data, isError, isLoading}) => {

  const nodes = data.filter(item => item.group === "nodes").map(item => ({
    id: item.data.id, 
    label: item.data.name, 
    group: item.group, 
    classes: item.classes
  }));

  const edges = data.filter(item => item.group === "edges").map(item => ({
    id: item.id,
    group: item.group,
    from: item.data.source, 
    to: item.data.target,
    weight: item.data.llr,
    label: item.data.action
  }));

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
  <Divider/>
  <Heading size='md' my={4}>Nodes</Heading>
  <Table bg="white" borderRadius={5}>
    <Thead>
      <Tr>
      {nodeCols.map((col) => (
        <Th key={col.id}>{col.name}</Th>
      ))}
      </Tr>
    </Thead>
    <Tbody>
      {nodes.map((item) => (
        <Tr key={item.id}>
          <Td>
            <Text className="capitalize" fontWeight="medium">{item.id}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.group}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.label}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.classes}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  <Heading size='md' my={4}>Edges</Heading>
  <Table bg="white" borderRadius={5}>
    <Thead>
      <Tr>
      {edgeCols.map((col) => (
        <Th key={col.id}>{col.name}</Th>
      ))}
      </Tr>
    </Thead>
    <Tbody>
      {edges.map((item) => (
        <Tr key={item.id}>
          <Td>
            <Text className="capitalize" fontWeight="medium">{item.id}</Text>
          </Td>
          <Td>
           <Text color="muted">{item.group}</Text>
          </Td>
          <Td>
          {typeof item.weight === "number" ? (
              <Text color="muted">{item.weight.toFixed(2)}</Text>
            ) : (
              <Text color="error">No value</Text>
            )}
          </Td>
          <Td>
            <Text color="muted">{item.from}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.label}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.to}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default PathTable