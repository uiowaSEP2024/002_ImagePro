import React from 'react';
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

export default function SignUp() {
  return (
    <div>
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
            css={{ mb: '6px' }}
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
            css={{ mb: '6px' }}
          />
          <Row justify="space-between">
          <Link block color="secondary" href="/login">Existing user? Log in. </Link>
          </Row>
          <Spacer y={1} />
          <Button>Create Account</Button>
        </Card>
      </Container>
    </div>
  );
}