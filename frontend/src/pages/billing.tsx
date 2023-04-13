import { Text, Grid } from "@nextui-org/react";
import { withAuthenticated } from "@/components/withAuthenticated";

function Billing() {

  return (
    <>
      <Grid.Container gap={2} justify="center">
        <Text h1 align-items="center">
          Billing page
        </Text>
      </Grid.Container>
    </>
  );
}

export default withAuthenticated(Billing)