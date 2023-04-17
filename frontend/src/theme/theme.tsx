import { extendTheme, ThemeConfig, ThemeOverride } from "@chakra-ui/react";

export const themeConfig: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false
};

const themeOverride: ThemeOverride = {
  config: themeConfig
};

export const theme = extendTheme(themeOverride);
