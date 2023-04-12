import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import {
  Card,
  Spacer,
  Button,
  Text,
  Input,
  Row,
  Link,
  Container,
} from "@nextui-org/react";
import { checkUserLoggedIn, fetchSignUp } from "@/utils/auth";

export default function SignUp() {
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  const router = useRouter();
  const [data, setData] = useState(null);

  useEffect(() => {
    checkUserLoggedIn()
      .then((data) => {
        setData(data.message);
        console.log(data.message);
        if (data == "already logged in!") {
          router.push("/");
        }
      })
      .catch((error) => {
        router.push("/");
        console.log(error);
      });
  }, [router]);

  const sendSignUpReq = () => {
    if (confirmPassword !== password) {
      console.log("Passwords Do Not Match");
      return;
    }

    fetchSignUp(email, password, first_name, last_name)
      .then((data) => {
        setNotificationMessage("Sign up successful!");
        router.push("/dashboard")
        console.log("hiiii", data);
      })
      .catch((e) => {
        console.log(e);
        setNotificationMessage("Sign up failed!");
      });
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
