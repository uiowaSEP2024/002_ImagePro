import { Grid, Container, Text, Spacer } from "@nextui-org/react";
// import { Cookies } from 'react-cookie';
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";



export default function Profile() {
  const {currentUser} = useAuthContext()

  useEnsureAuthenticated()
 
  return (
    <Container>
      <Grid.Container gap={2} justify="center">
        <Grid xs={12} md={6}>
          <Text h4>First Name</Text>
          <Spacer x={1} />
          <Text>{currentUser?.first_name}</Text>
        </Grid>
        <Grid xs={12} md={6}>
          <Text h4>Last Name</Text>
          <Spacer x={1} />
          <Text>{currentUser?.last_name}</Text>
        </Grid>
        <Grid xs={12}>
          <Text h4>Email</Text>
          <Spacer x={1} />
          <Text>{currentUser?.email}</Text>
        </Grid>
      </Grid.Container>
    </Container>
  );
}
