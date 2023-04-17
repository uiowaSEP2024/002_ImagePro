import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
// 1. import `NextUIProvider` component
import { AuthContextProvider } from "@/contexts/authContext";
import { ChakraProvider } from "@chakra-ui/react";
import { NextUIProvider } from "@nextui-org/react";
import { theme } from "@/theme/theme";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <NextUIProvider>
      <ChakraProvider theme={theme}>
        <AuthContextProvider>
          {/* Render the Navbar */}
          <Navbar />
          {/* Render the page */}
          <Component {...pageProps} />
        </AuthContextProvider>
      </ChakraProvider>
    </NextUIProvider>
  );
}

export default MyApp;
