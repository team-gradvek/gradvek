import { extendTheme, theme as baseTheme } from "@chakra-ui/react";
import { theme as gradvekTheme } from '@chakra-ui/pro-theme'
import '@fontsource/fira-code'

// palette https://mycolor.space/?hex=%232E1B4E&sub=1 - matching gradient section

export const theme = extendTheme({
  initialColorMode: 'light',
  useSystemColorMode: false,
  colors:{ ...baseTheme.colors, brand: baseTheme.colors.blue },
  fonts: {
    heading: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
    body: `'Fira CodeVariable', -apple-system, system-ui, sans-serif`,
  }, 
  brand: {
    color: "#15417D",
    secondary: "#0069A4",
    purple: "#2E1B4E"
  },
  gradvekTheme,
});
export default theme;