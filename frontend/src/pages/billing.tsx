import { Text, Grid } from "@nextui-org/react";
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";

export default function Billing() {
  const router = useRouter();
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      setData(data.detail)
      console.log(data.detail)
      if (data == "Not authenticated") {
        router.push('/login')
      }
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
