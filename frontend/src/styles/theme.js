import { extendTheme } from "@chakra-ui/react";
import '@fontsource/fira-code'

export const theme = extendTheme({
  initialColorMode: "light",
  useSystemColorMode: false,
  colors:{
    gradvekblue:{
      400: '#47819d'
    }
  },
  fonts: {
    heading: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
    body: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
  }
});
export default theme;