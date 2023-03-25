import { Grid, Container, Text } from "@nextui-org/react";
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
      <Container>
        <Grid.Container gap={2} justify="center">
          <Grid xs={12} md={6}>
            <Text h4>First Name</Text>
            <Text>{first_name}</Text>
          </Grid>
          <Grid xs={12} md={6}>
            <Text h4>Last Name</Text>
            <Text>{last_name}</Text>
          </Grid>
          <Grid xs={12}>
            <Text h4>Email</Text>
            <Text>{email}</Text>
          </Grid>
        </Grid.Container>
      </Container>
    );
  } 
}