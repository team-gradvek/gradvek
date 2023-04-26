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
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Card, CardBody, 
} from '@chakra-ui/react'
import Link from 'next/link'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
// import getAdverseEvent from "../../hooks/targetToAdverseEventHook"


const MouseTable = ({data, title, columns}) => {

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
            <Text className="capitalize" fontWeight="medium">{item.target1}</Text>
          </Td>
          <Td>
            <Text className="capitalize" fontWeight="medium"><Link href='/targetToAdverseEvent/{item.target2}'>{item.target2}</Link></Text>
          </Td>
          <Td>
           <Text color="muted">{item.similarity}</Text>
          </Td>
          <Td>
           <Text color="muted">Mouse Phenotype</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default MouseTable