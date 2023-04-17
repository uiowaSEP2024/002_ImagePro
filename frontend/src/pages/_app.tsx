import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
import { AuthContextProvider } from "@/contexts/authContext";
import { ChakraProvider } from "@chakra-ui/react";
import { NextUIProvider } from "@nextui-org/react";
import { theme } from "@/theme/theme";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider theme={theme}>
      <NextUIProvider>
        <AuthContextProvider>
          {/* Render the Navbar */}
          <Navbar />
          {/* Render the page */}
          <Component {...pageProps} />
        </AuthContextProvider>
      </NextUIProvider>
    </ChakraProvider>
  );
}

export default MyApp;
