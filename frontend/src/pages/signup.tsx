import React, {useState} from "react";
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

export default function SignUp() { 

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  const sendSignupReq = () => {
    if(confirmPassword !== password) {
      console.log("Passwords Do Not Match")
      return
    }
  
    fetch("http://localhost:8000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        data: {
          email: email,
          passsword: password
        },
      }),
    })
      .then(response => response.json())
      .then(data => console.log(data));
  
  }

  return (
    <div>
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
            onChange={e => setEmail(e.target.value)}
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
            css={{ mb: "6px" }}
            value={password}
            onChange={e => setPassword(e.target.value)}
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
            css={{ mb: "6px" }}
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
          />
          <Row justify="space-between">
            <Link block color="secondary" href="/login">Existing user? Log in. </Link>
          </Row>
          <Spacer y={1} />
          <Button onClick={sendSignupReq}>Create Account</Button>
        </Card>
      </Container>
    </div>
  );
}