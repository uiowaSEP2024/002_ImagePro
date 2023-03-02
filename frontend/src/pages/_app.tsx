import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Navbar from "src/components/Navbar";
// 1. import `NextUIProvider` component
import { NextUIProvider } from "@nextui-org/react";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <NextUIProvider>
      {/* Render the Navbar */}
      <Navbar />
      {/* Render the page */}
      <Component {...pageProps} />
    </NextUIProvider>
  );
}

export default MyApp;
