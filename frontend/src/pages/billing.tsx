import { Container, Heading, Text } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";

function Billing() {
  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <Heading lineHeight={1.5} textAlign={"center"}>
        Billing
      </Heading>
      <Text textAlign={"center"}>Coming soon...</Text>
    </Container>
  );
}

export default withAuthenticated(Billing, ["provider"]);
