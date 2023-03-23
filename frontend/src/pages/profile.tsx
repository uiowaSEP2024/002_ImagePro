import { Text, Grid } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";

export default function Profile() {
  const router = useRouter();
  const [msg, setMsg] = useState(null)
  const [data, setData] = useState(null)

  const redirect = () => {
    router.push("/login")
  }

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      setData(data.user.first_name)
      setMsg(data.message)
    })
  })

  if (msg != "already logged in!") {
    return (
      redirect()
    );
  } else {
    return (
      <>
        <Grid.Container gap={2} justify="center">
          <Text h1 align-items="center">
            Profile for { data }
          </Text>
        </Grid.Container>
      </>
    );
  } 
}