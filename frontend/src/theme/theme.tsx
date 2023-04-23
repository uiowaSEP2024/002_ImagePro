import { extendTheme, ThemeConfig, ThemeOverride } from "@chakra-ui/react";
import { DM_Sans } from "@next/font/google";

export const themeConfig: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false
};

const breakpoints = {
  sm: "30em",
  md: "48em",
  lg: "62em",
  xl: "80em",
  "2xl": "96em"
};

export const fontPrimary = DM_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "700"]
});
const themeOverride: ThemeOverride = {
  config: themeConfig,
  fonts: {
    body: fontPrimary.style.fontFamily,
    heading: fontPrimary.style.fontFamily
  },
  breakpoints,
  components: {
    Button: {
      baseStyle: {
        fontWeight: "bold",
        color: "white"
      },
      sizes: {
        xl: {
          h: "56px",
          fontSize: "lg",
          px: "32px"
        }
      },
      variants: {
        "with-shadow": {
          bg: "#2600BF",
          boxShadow: "0 0 2px 2px #efdfde"
        },
        delete: {
          fontWeight: "normal",
          color: "white",
          backgroundColor: "red.500"
        },
        sm: {
          bg: "#2600BF",
          fontSize: "md"
        }
      },
      defaultProps: {
        size: "lg",
        variant: "sm",
        colorScheme: "#2600BF"
      }
    }
  }
};

export const theme = extendTheme(themeOverride);
