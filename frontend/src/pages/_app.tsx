import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
// 1. import `NextUIProvider` component
import { NextUIProvider } from "@nextui-org/react";
import { AuthContextProvider } from "@/contexts/authContext";

function MyApp({ Component, pageProps }: AppProps) {


  return (
    <NextUIProvider>
    

      <AuthContextProvider>
        {/* Render the Navbar */}
        <Navbar />
        {/* Render the page */}
        <Component {...pageProps} />
      </AuthContextProvider>
    </NextUIProvider>
  );
}

export default MyApp;
