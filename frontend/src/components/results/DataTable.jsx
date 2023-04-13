import {
  Avatar,
  Box,
  Checkbox,
  HStack,
  Icon,
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
import { IoArrowDown } from 'react-icons/io5'
import { events } from '../data/FetchAdverseEventData'
import DrugTable from './DrugTable'


const DataTable = (props) => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  return (
  <>
  <Table {...props} bg="white" borderRadius={5}>
    <Thead>
      <Tr>
        <Th>
          <HStack spacing="3">
            <Checkbox />
            <HStack spacing="1">
              <Text>Adverse Event</Text>
              <Icon as={IoArrowDown} color="muted" boxSize="4" />
            </HStack>
          </HStack>
        </Th>
        <Th>Associated Drugs</Th>
        <Th>Weight</Th>
      </Tr>
    </Thead>
    <Tbody>
      {events.map((event) => (
        <Tr key={event.id}>
          <Td>
            <HStack spacing="3">
              <Checkbox />
              <Avatar name={event.name} boxSize="10" />
              <Box>
                <Text fontWeight="medium">{event.name}</Text>
              </Box>
            </HStack>
          </Td>
          <Td>
            <Button variant="ghost" colorScheme="blue" onClick={onOpen}>Open AE Drugs</Button>
          </Td>
          <Td>
            <Text color="muted">{event.llr}</Text>
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
            <DrugTable/>
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