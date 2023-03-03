import { Button, Link, Spacer, Text, Textarea, Container, Col, Row } from "@nextui-org/react";

export default function SignUp() {
  return (
    <Container align-content="center" >
      <Row>
        <Col/>
        <Col>
          <Spacer y={1} />
          <Text h3>Create Account</Text>
          <Spacer y={1}/>
          <Container justify="center" >
          <Textarea
              underlined
              color="primary"
              labelPlaceholder="First Name"
            />
          <Spacer y={1}/>
          <Textarea
              underlined
              color="primary"
              labelPlaceholder="Last Name"
            />
          <Spacer y={1} />
          <Textarea
              underlined
              color="primary"
              labelPlaceholder="Email"
            />
          </Container>
          <Spacer y={1}/>
          <Button flat color="primary" auto>
            Sign Up
          </Button>
          <Spacer y={1}/>
          <Link block color="secondary" href="#">
            Existing user? Go to Login
          </Link>
        </Col>
        <Col/>
        <Col/>
      </Row>
    </Container>

  )
}