import { Text } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { checkUserLoggedIn } from "@/utils/auth";

import { Card, Container, Link } from "@nextui-org/react";

export default function Dashboard() {
  const router = useRouter();
  const [data, setData] = useState(null);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    checkUserLoggedIn()
        .then((data) => {
            setData(data.user.first_name);
        })
        .catch((error) => {
            router.push("/login");
            console.log(error);
        });
}, [router]);

  return (
    <>
      <Container gap={2} justify="center">
        <Text h1 align-items="center">
          Welcome {data}
        </Text>

        <Card>
          <Card.Header>
            <Link css={{ display: "block", width: "100%" }} href="/jobs">
              <Text h3>Jobs ↗️</Text>
            </Link>
          </Card.Header>
          <Card.Body>
            <Text>View past and currently active jobs</Text>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
}
