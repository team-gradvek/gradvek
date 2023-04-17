import { Checkbox, Stack, Text} from '@chakra-ui/react'

function countSetToZero(action) {
  return action.count > 0;
}

export const Actions = ({title, checkboxArray}) => {

  const filteredActions = checkboxArray.filter(countSetToZero)

  return (
  <Stack spacing={[2]} direction={['column']}>
    <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
      {title}
    </Text>
    {filteredActions.map((action) => (
        <Checkbox size='md' colorScheme='blue' key={action.action} id={action.action} value={action.action} defaultChecked>
          {action.action} ({action.count})
        </Checkbox>
    ))}
  </Stack>
  )
}