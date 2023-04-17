import { Checkbox, Stack, Text, Divider} from '@chakra-ui/react'

export const Descriptors = ({title, checkboxArray}) => {
  if (checkboxArray.length !== 0 )
    return (
    <Stack spacing={[1, 2]} direction={['column']}>
        <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
              {title}
            </Text>
      {checkboxArray.map((item) => (
      <Checkbox size='md' colorScheme='blue' id={ item.name } >
        { item.name }
      </Checkbox>
      ))}
    </Stack>
    )
}