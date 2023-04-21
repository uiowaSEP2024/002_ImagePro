import React from "react";
import { useState } from "react";
import { useRouter } from "next/router";
import { Flex, Text, Box, Input, Button, InputGroup, InputRightElement, Link } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons"
import { useAuthContext } from "@/hooks/useAuthContext";
import { withUnauthenticated } from "@/components/withAuthenticated";

function Login() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false)
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
    <Flex direction='column' padding='30px'>
      {!!notificationMessage && <Text>{notificationMessage}</Text>}
      <Text fontSize='36px' as='b' marginBottom='10px'>Login</Text>
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>Email</Text>
        <Input variant='filled' size='sm' placeholder="First Name" value={email} onChange={(e) => setEmail(e.target.value)}/>
      </Box>
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>Password</Text>
        <InputGroup>
          <Input variant='filled' size='sm' placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} type={showPassword ? "text" : "password"}/>
          <InputRightElement width='4.0rem' height='2.0rem'>
            <Button h='1.5rem' size='xs' onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? "Hide" : "Show"}
            </Button>
          </InputRightElement>
        </InputGroup>
      </Box>
      <Box flex='1' w='100px' marginBlock='10px'>
        <Button size='sm' name="signup" role="button" data-testid="signup" onClick={handleLogin}>Login</Button>
      </Box>
      <Link w='fit-content' href="/signup">
        New user? Create an account. <ExternalLinkIcon mx='2px' mb='2px' />
      </Link>
    </Flex>
  );
}

export default withUnauthenticated(Login);
