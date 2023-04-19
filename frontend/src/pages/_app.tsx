import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
import { AuthContextProvider } from "@/contexts/authContext";
import { ChakraProvider } from "@chakra-ui/react";
import { NextUIProvider } from "@nextui-org/react";
import { appFont, theme } from "@/theme/theme";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className={appFont.className}>
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
    </div>
  );
}

export default MyApp;
