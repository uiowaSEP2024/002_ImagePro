import { Container, Heading, Spacer } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";
import JobsChart from "@/components/stackedChart";

function Billing() {
  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <Heading lineHeight={1.5} textAlign={"center"}>
        Billing
      </Heading>
      <Spacer height='20px' />
      {/* <Text textAlign={"center"}>Coming soon...</Text> */}
      <JobsChart />
    </Container>
  );
}

export default withAuthenticated(Billing, ["provider"]);
