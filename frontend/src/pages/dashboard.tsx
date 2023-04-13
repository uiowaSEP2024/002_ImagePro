import { Text } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';

import { Card, Container, Link } from "@nextui-org/react";
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";



export default function Dashboard() {

  const {currentUser} = useAuthContext()

  useEnsureAuthenticated()

  return (
    <>
      <Container gap={2} justify="center">
        <Text h1 align-items="center">
          Welcome {currentUser?.first_name}
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
