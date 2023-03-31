import { extendTheme } from "@chakra-ui/react";

export const theme = extendTheme({
  initialColorMode: "dark",
  useSystemColorMode: false,
  colors:{
    gradvekblue:{
      400: '#47819d'
    }
  },
  components: {
    Tabs: {
      baseStyle: {
        tab: {
          color: "blue.600",
          _selected: {
            bg: 'red',
          }
        }
      }
    }
  }
});
export default theme;