import { Grid, Container, Text, Spacer } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { checkUserLoggedIn } from "@/utils/auth";

export default function Profile() {
  const [first_name, setFirst_Name] = useState(null);
  const [last_name, setLast_Name] = useState(null);
  const [email, setEmail] = useState(null);
  const router = useRouter();
  const [msg, setMsg] = useState(null);
  // const [data, setData] = useState(null)

  useEffect(() => {
    checkUserLoggedIn()
      .then((data) => {
        setFirst_Name(data.user.first_name);
        setLast_Name(data.user.last_name);
        setEmail(data.user.email)
      })
      .catch((error) => {
        router.push("/login");
        console.log(error);
      });
  }, [router]);

  return (
    <Container>
      <Grid.Container gap={2} justify="center">
        <Grid xs={12} md={6}>
          <Text h4>First Name</Text>
          <Spacer x={1} />
          <Text>{first_name}</Text>
        </Grid>
        <Grid xs={12} md={6}>
          <Text h4>Last Name</Text>
          <Spacer x={1} />
          <Text>{last_name}</Text>
        </Grid>
        <Grid xs={12}>
          <Text h4>Email</Text>
          <Spacer x={1} />
          <Text>{email}</Text>
        </Grid>
      </Grid.Container>
    </Container>
  );
}
