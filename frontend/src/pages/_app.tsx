import "@/styles/globals.css"
import type { AppProps } from "next/app"
import TopNavbar from "./navbar"
import Home from "./index"
// 1. import `NextUIProvider` component
import { NextUIProvider } from '@nextui-org/react';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      < TopNavbar />
      < Home />
    </>
  );
}

export default MyApp;