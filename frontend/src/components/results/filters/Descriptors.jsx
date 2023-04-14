import { Checkbox, Stack, Text} from '@chakra-ui/react'

export const Descriptors = (props) => {
  // const { checked } = props

  return (
  <Stack spacing={[1, 2]} direction={['column']}>
       <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
            Descriptors
          </Text>
    <Checkbox size='md' colorScheme='blue' id="Gene">
      Gene
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="Protein">
      Protein
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="GWAS">
      GWAS
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="Phenotype">
      Phenotype
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="Reactome">
      Reactome
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="Signor">
      Signor
    </Checkbox>
    <Checkbox size='md' colorScheme='blue' id="IntAct">
      IntAct
    </Checkbox>
  </Stack>
  )
}