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
  Divider,
} from '@chakra-ui/react'
import { IoArrowDown } from 'react-icons/io5'
import DrugTable from './DrugTable'

// @TODO Refactor this when request is made
import { drugs } from '../data/FetchDrugData'

const drugTableColumns = [
  {
    id: 1,
    name: 'Drug Name'
  }, 
  {
    id: 2,
    name: 'ID'
  }, 
  {
    id: 3,
    name: 'Weight'
  }
]


const DataTable = ({title, columns, data}) => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  if (typeof(data) === 'undefined' || typeof(columns) === 'undefined' ){
    return (
      <>
      <Heading size='md' mb={4}>No Data Found</Heading>
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
            <HStack spacing="3">
              <Checkbox />
              <Avatar name={item.name} boxSize="10" />
              <Box>
                <Text className="capitalize" fontWeight="medium">{item.name}</Text>
              </Box>
            </HStack>
          </Td>
          <Td>
            <Button variant="ghost" colorScheme="blue" onClick={onOpen}>Open AE Drugs</Button>
          </Td>
          <Td>
            <Text color="muted">{item.llr}</Text>
          </Td>
          <Td>
            <Text color="muted">{item.dataset}</Text>
          </Td>
        </Tr>
      ))}
    </Tbody>
  </Table>
  <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Associated Drugs</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box w="200px">
            <DrugTable 
              columns={drugTableColumns}
              data={drugs}
              />
            </Box>
          </ModalBody>
          <ModalFooter>
          </ModalFooter>
        </ModalContent>
      </Modal>
  </>
  )
}

export default DataTable