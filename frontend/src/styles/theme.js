import { extendTheme, theme as baseTheme } from "@chakra-ui/react";
import { theme as gradvekTheme } from '@chakra-ui/pro-theme'
import '@fontsource/fira-code'

export const theme = extendTheme({
  initialColorMode: "light",
  useSystemColorMode: false,
  colors:{ ...baseTheme.colors, brand: baseTheme.colors.blue },
  fonts: {
    heading: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
    body: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
  }, 
  brand: {
    blue: "#3D7692",
  },
  gradvekTheme,
});
export default theme;