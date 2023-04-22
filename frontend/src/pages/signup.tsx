import React, { useState } from "react";
import {
  Card,
  Spacer,
  Text,
  Input,
  Row,
  Link,
  Container,
  Button
} from "@nextui-org/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import { fetchSignUp } from "@/data";
import { withUnauthenticated } from "@/components/withAuthenticated";

function SignUp() {
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  const { logIn } = useAuthContext()


  const sendSignUpReq = async () => {
    if (confirmPassword !== password) {
      console.log("Passwords Do Not Match");
      return;
    }

    try{
      const data = await fetchSignUp({
        email,
        first_name,
        last_name,
        password
      })
      console.log(data)
      setNotificationMessage("Sign up successful! Logging you in...");
      await logIn(email, password)
    }catch(e){
      console.log(e);
      setNotificationMessage("Sign up failed!");
    }
  };

  return (
    <div>
      {!!notificationMessage && <Text data-test-id='notification-message'>{notificationMessage}</Text>}
      <Container
        display="flex"
        alignItems="center"
        justify="center"
        css={{ minHeight: "100vh" }}
      >
        <Card css={{ mw: "420px", p: "20px" }} variant="bordered">
          <Text
            size={24}
            weight="bold"
            h1
            align-items="center"
            css={{
              as: "center",
              mb: "20px",
            }}
          >
            Sign Up
          </Text>
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="First Name"
            aria-label="First Name"
            value={first_name}
            onChange={(e) => setFirstName(e.target.value)}
          />
          <Spacer y={1} />
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Last Name"
            aria-label="Last Name"
            value={last_name}
            onChange={(e) => setLastName(e.target.value)}
          />
          <Spacer y={1} />
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Email"
            aria-label="Email"
            css={{ mb: "6px" }}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Spacer y={1} />
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Password"
            aria-label="Password"
            type="password"
            css={{ mb: "6px" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Spacer y={1} />
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Confirm Password"
            aria-label="Confirm Password"
            type="password"
            css={{ mb: "6px" }}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <Row justify="space-between">
            <Link block color="secondary" href="/login">
              Existing user? Log in.{" "}
            </Link>
          </Row>
          <Spacer y={1} />
          <Button name="signup" role="button" data-testid="signup" onPress={sendSignUpReq}>Create Account</Button>
        </Card>
      </Container>
    </div>
  );
}


export default withUnauthenticated(SignUp)
