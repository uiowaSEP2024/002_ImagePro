import { Text } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';

import { Card, Container, Link } from "@nextui-org/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";



function Dashboard() {
  const {currentUser} = useAuthContext()


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
            <Text role="text">View past and currently active jobs</Text>
          </Card.Body>
        </Card>
        <Text h1 align-items="center">
          Statistics
        </Text>
      </Container>
    </>
  );
}

export default withAuthenticated(Dashboard)