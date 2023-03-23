import { Text, Grid } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";

export default function Profile() {
  const [first_name, setFirst_Name] = useState(null)
  const [last_name, setLast_Name] = useState(null)
  const [email, setEmail] = useState(null)
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
      setFirst_Name(data.user.first_name)
      setLast_Name(data.user.last_name)
      setEmail(data.user.email)
      setMsg(data.detail)
    })
  })

  if (msg == "Not authenticated") {
    return (
      redirect()
    );
  } else {
    return (
      <>
        <Grid.Container gap={2} justify="center">
          <Text h1 align-items="center">
            Profile for { first_name } { last_name }
            Email: { email }
          </Text>
        </Grid.Container>
      </>
    );
  } 
}