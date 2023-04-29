import { Container, Heading } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";

function Billing() {
  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <Heading textAlign={"center"}>Billing page</Heading>
    </Container>
  );
}

export default withAuthenticated(Billing, ["provider"]);
