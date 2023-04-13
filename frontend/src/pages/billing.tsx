import { Text, Grid } from "@nextui-org/react";
import { useEnsureAuthenticated } from "@/hooks/useAuthContext";

export default function Billing() {
  useEnsureAuthenticated()

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
