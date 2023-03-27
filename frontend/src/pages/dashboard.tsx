import { Text, Card, Container, Link } from "@nextui-org/react";

export default function Dashboard() {
  return (
    <>
      <Container gap={2} justify="center">
        <Text h1 align-items="center">
          Dashboard page
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
