import { Checkbox, Stack, Text} from '@chakra-ui/react'
import { actions } from '@/components/data/FetchActionsData'

const filteredActions = actions.filter(countSetToZero)

function countSetToZero(action) {
  return action.count > 0;
}

console.log(filteredActions)

export const Actions = (props) => {

  return (
  <Stack spacing={[1, 2]} direction={['column']}>
    <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
      Actions
    </Text>
    {filteredActions.map((action) => (
        <Checkbox size='md' colorScheme='blue' key= {action.action} id={action.action} value={action.action} defaultChecked>
          {action.action} ({action.count})
        </Checkbox>
    ))}
  </Stack>
  )
}