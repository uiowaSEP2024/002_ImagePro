import { Text, Grid } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";


export default function Dashboard() {
  const router = useRouter();
  const [data, setData] = useState(null)
  const [msg, setMsg] = useState(null)

  const redirect = () => {
    router.push("/login")
  }

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      // console.log(data.status_code)
      if('detail' in data) {
        setMsg(data.detail)
        console.log(data.detail)
      }
      else {
        setData(data.user.first_name)
      }
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
            Welcome {data}
          </Text>
        </Grid.Container>
      </>
    );
  }
}


// export async function getServerSideProps() {
//   const cookie = new Cookies()
//   const result = await fetch("http://localhost:8000/login", {
//     credentials: "include",
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     // body: {cookie.get('Value')}
//   })
//   const data = result.json()

//   return { props: { data } }
// }

// export default Dashboard

