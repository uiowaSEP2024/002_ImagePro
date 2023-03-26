import React from "react";
import { useState, useEffect } from "react";
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

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [data, setData] = useState(null)

  const [notificationMessage, setNotificationMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      setData(data.message)
      console.log(data.message)
      if (data == "already logged in!") {
        router.push("/")
      }
    })
  })

  const sendLoginReq = () => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      },
      body: new URLSearchParams({
        username: email,
        password: password,
      }),
    })
      .then((response) => {
        if (response.status == 200) {
          setNotificationMessage("Login successful. Redirecting...");
          router.push("/dashboard");
        }
      })
      .catch((e) => {
        console.log(e);
      });
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
            css={{
              as: "center",
              mb: "20px",
            }}
          >
            Login
          </Text>
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Email"
            aria-label="Email"
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
          <Button onPress={sendLoginReq}>Log in</Button>
        </Card>
      </Container>
    </div>
  );

}
