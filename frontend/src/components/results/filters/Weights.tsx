import { Box, RangeSlider, RangeSliderFilledTrack, RangeSliderMark, RangeSliderThumb, RangeSliderTrack, Text} from '@chakra-ui/react'
import React, { useState } from 'react';



function WeightSlider( props ) {
  const [sliderValue, setSliderValue] = useState([25, 75])
  return (
    <>
    <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
      Adverse Events
    </Text>
    <RangeSlider aria-label={['min', 'max']} defaultValue={[25, 75]} onChange={(val) => setSliderValue(val)}>
      <RangeSliderMark value={0} mt='1' ml='-2.5' fontSize='sm'>
        0
      </RangeSliderMark>
      <RangeSliderMark value={50} mt='1' ml='-2.5' fontSize='sm'>
        0.50
      </RangeSliderMark>
      <RangeSliderMark value={100} mt='1' ml='-2.5' fontSize='sm'>
       1
      </RangeSliderMark>
      <RangeSliderTrack>
        <RangeSliderFilledTrack bg='blue.500' />
      </RangeSliderTrack>
      <RangeSliderThumb boxSize={6} index={0}>
        <Box color='tomato' />
      </RangeSliderThumb>
      <RangeSliderThumb boxSize={6} index={1}>
        <Box color='tomato' />
      </RangeSliderThumb>
    </RangeSlider>
    </>
  )
}


export default WeightSlider;
