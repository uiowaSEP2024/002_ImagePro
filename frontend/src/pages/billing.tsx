import { Container, Heading, Text } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";

function Billing() {
  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <Heading lineHeight={1.5} textAlign={"center"}>
        Billing
      </Heading>
      <Text fontSize={"2xl"} textAlign={"center"}>
        Under construction...
      </Text>
      <Heading fontSize={"8xl"} mt={"20vh"} textAlign={"center"}>
        🏗️
      </Heading>
    </Container>
  );
}

export default withAuthenticated(Billing, ["provider"]);
