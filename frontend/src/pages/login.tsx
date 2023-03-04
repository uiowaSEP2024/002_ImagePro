import React, { useState } from "react";
import {
  Card,
  Spacer,
  Button,
  Text,
  Input,
  Row,
  Link,
  Container,
} from '@nextui-org/react';

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  
  const sendSignUpReq = () => {
    fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      },
      body: new URLSearchParams({
        'username': email,
        'password': password
      })
    })
    .then((response) => {
      if(response.status == 200){
        console.log("Success")
      }
    })
  }


  return (
    <div>
      {!!notificationMessage && <Text>{notificationMessage}</Text>}
      <Container
        display="flex"
        alignItems="center"
        justify="center"
        css={{ minHeight: '100vh' }}
      >
        <Card css={{ mw: '420px', p: '20px' }} variant="bordered">
          <Text
            size={24}
            weight="bold"
            css={{
              as: 'center',
              mb: '20px',
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
            css={{ mb: '6px' }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Row justify="space-between">
          <Link block color="secondary" href="/signup">New user? Create Account. </Link>
          </Row>
          <Spacer y={1} />
          <Button onPress={sendSignUpReq}>Log in</Button>
        </Card>
      </Container>
    </div>
  );
}