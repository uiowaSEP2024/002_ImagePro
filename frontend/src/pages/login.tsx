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

export default function Login() {
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
            Login
          </Text>
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Email"
          />
          <Spacer y={1} />
          <Input
            clearable
            underlined
            fullWidth
            color="primary"
            size="lg"
            placeholder="Password"
            css={{ mb: '6px' }}
          />
          <Row justify="space-between">
          <Link block color="secondary" href="/signup">New user? Create Account. </Link>
          </Row>
          <Spacer y={1} />
          <Button>Log in</Button>
        </Card>
      </Container>
    </div>
  );
}