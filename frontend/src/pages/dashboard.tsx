import { Text, Grid } from "@nextui-org/react";
import { Cookies } from 'react-cookie';



function Dashboard() {
  return (
    <>
      <Grid.Container gap={2} justify="center">
        <Text h1 align-items="center">
          Dashboard page
        </Text>
      </Grid.Container>
    </>
  );
}


export async function getServerSideProps() {
  const cookie = new Cookies()
  const result = await fetch("http://localhost:8000/login", {
    credentials: "include",
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    // body: {cookie.get('Value')}
  })
  const data = result.json()

  return { props: { data } }
}

export default Dashboard

