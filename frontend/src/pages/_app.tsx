import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
// 1. import `NextUIProvider` component
import { ChakraProvider } from "@chakra-ui/react";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      {/* Render the Navbar */}
      <Navbar />
      {/* Render the page */}
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default MyApp;
