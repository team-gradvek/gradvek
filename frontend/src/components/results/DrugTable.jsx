import {
  Avatar,
  Box,
  Checkbox,
  HStack,
  Icon,
  IconButton,
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
} from '@chakra-ui/react'
import { drugs } from '../data/FetchDrugData'


const DrugTable = (props) => {
  return (
  <>
  <Table {...props} bg="white" borderRadius={5}>
    <Thead>
      <Tr>
        <Th>Drug Name</Th>
        <Th>ID</Th>
        <Th>Weight</Th>
      </Tr>
    </Thead>
    <Tbody>
      {drugs.map((drug) => (
        <Tr key={drug.drugId}>
          <Td>
            <Text fontWeight="bold">{drug.drugName}</Text>
          </Td>
          <Td>
            <Text>{drug.drugId}</Text>
          </Td>
          <Td>
            <Text>{drug.weight}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  </>
  )
}

export default DrugTable