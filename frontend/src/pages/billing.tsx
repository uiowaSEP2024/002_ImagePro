import { Text, Grid } from "@nextui-org/react";
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";
import { checkUserLoggedIn } from "@/utils/auth";

export default function Billing() {
  const router = useRouter();

  useEffect(() => {
    checkUserLoggedIn().then((data) => {
      if (data.detail == "Not authenticated") {
        router.push('/login')
      }
    }).catch((error) => {
      router.push('/login')
      console.log(error)
    })
  })

  return (
    <>
      <Grid.Container gap={2} justify="center">
        <Text h1 align-items="center">
          Billing page
        </Text>
      </Grid.Container>
    </>
  );
}
