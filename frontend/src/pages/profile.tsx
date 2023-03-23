import { Text, Grid } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from 'react';

export default function Profile() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      setData(data.user.first_name)
      
    })
  })
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