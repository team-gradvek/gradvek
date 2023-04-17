import { Box, RangeSlider, RangeSliderFilledTrack, RangeSliderMark, RangeSliderThumb, RangeSliderTrack, Text} from '@chakra-ui/react'
import React, { useState } from 'react';



function WeightSlider({ title, range, initial }) {
  const [sliderValue, setSliderValue] = useState([25, 75])
  return (
    <>
    <Text fontSize="lg" color="on-accent-muted" fontWeight="medium">
      {title}
    </Text>
    <RangeSlider aria-label={['min', 'max']} defaultValue={[initial.min, initial.max]} onChange={(val) => setSliderValue(val)}>
      <RangeSliderMark value={range.min} mt='1' ml='-2.5' fontSize='sm'>
        {range.min}
      </RangeSliderMark>
      <RangeSliderMark value={range.mid} mt='1' ml='-2.5' fontSize='sm'>
        {range.mid}
      </RangeSliderMark>
      <RangeSliderMark value={range.max} mt='1' ml='-2.5' fontSize='sm'>
       {range.max}
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
