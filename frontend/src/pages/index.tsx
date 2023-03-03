import Head from "next/head"
import { Inter } from "@next/font/google"
import styles from "@/styles/Home.module.css"
import { Text, Container, Grid, Spacer } from "@nextui-org/react";

const inter = Inter({ subsets: ["latin"] })

export default function Home() {
  return (
    <>
      <Head>
        <title>BotImage Tracking App Team 03</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Spacer/>
      <Grid.Container gap={2} justify="center">
          <Text h1 align-items="center">Welcome to the tracking site.</Text>
      </Grid.Container>
    </>
  )
}
