import React from "react";
import { useState } from "react";
import { useRouter } from "next/router";
import {
  Card,
  Spacer,
  Button,
  Text,
  Input,
  Link,
  Container,
  Row
} from "@nextui-org/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import { withUnauthenticated } from "@/components/withAuthenticated";

function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  const { logIn } = useAuthContext();

  const handleLogin = async () => {
    try {
      const result = await logIn(email, password);
      if (result && result.user) {
        setNotificationMessage("Login successful. Redirecting...");
        router.push("/dashboard");
      }
    } catch (e) {
      console.log(e);
      setNotificationMessage("Login failed. Please try again.");
    }
  };

  return (
    <div>
      {!!notificationMessage && <Text>{notificationMessage}</Text>}
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
              mb: "20px"
            }}
          >
            Login
          </Text>
          <Input
            color="primary"
            size="lg"
            placeholder="Email"
            aria-label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Spacer y={1} />
          <Input
            color="primary"
            size="lg"
            placeholder="Password"
            aria-label="Password"
            type={"password"}
            css={{ mb: "6px" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Row justify="space-between">
            <Link block color="secondary" href="/signup">
              New user? Create Account.{" "}
            </Link>
          </Row>
          <Spacer y={1} />
          <Button onPress={handleLogin}>Log in</Button>
        </Card>
      </Container>
    </div>
  );
}

export default withUnauthenticated(Login);
