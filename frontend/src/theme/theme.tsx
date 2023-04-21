import { extendTheme, ThemeConfig, ThemeOverride } from "@chakra-ui/react";

export const themeConfig: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false
};

const themeOverride: ThemeOverride = {
  config: themeConfig,
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
        regular: {
          bg: "#2600BF",
          fontSize: "md"
        }
      },
      defaultProps: {
        size: "lg",
        variant: "regular",
      }
    }
  }
};

export const theme = extendTheme(themeOverride);
