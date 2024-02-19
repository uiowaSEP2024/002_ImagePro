import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { AuthContextProvider } from "@/contexts/authContext";
import { ChakraProvider, Flex } from "@chakra-ui/react";
import { fontPrimary, theme } from "@/theme/theme";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className={fontPrimary.className}>
      <ChakraProvider theme={theme}>
        <AuthContextProvider>
          <Flex minH={"100vh"} direction="column">
            <Navbar />
            <Flex minH={"90vh"} direction={"column"} flex={1}>
              <Component {...pageProps} />
            </Flex>
            <Footer />
          </Flex>
        </AuthContextProvider>
      </ChakraProvider>
    </div>
  );
}

export default MyApp;
