import React from "react";
import { useState } from "react";
import { useRouter } from "next/router";
import {AiFillEye, AiFillEyeInvisible} from "react-icons/ai";
import { Container, Icon, IconButton, Text, Box, Input, Button, InputGroup, InputRightElement, Link, Center, VStack } from "@chakra-ui/react";
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

  const handleLogin = async (e) => {
    e.preventDefault()
    console.log("Submit")
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
    <Container display={"flex"} justifyContent={"center"} maxW={"container.lg"} py={"6"}>
      <Center maxW={"xs"} display="flex" flexDirection='column' paddingTop={"20vh"}>
        {!!notificationMessage && <Text>{notificationMessage}</Text>}
        <form onSubmit={handleLogin}> 
          <VStack spacing={4}>
            <Text role="heading" fontSize='36px' as='b' marginBottom='10px'>Login</Text>
            <Box w={"100%"} flex={1} bg='white' marginBlock='5px'>
              <Text fontSize='lg' fontWeight='500'>Email</Text>
              <Input variant='outline' placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
            </Box>
            <Box flex={1}  w={"100%"}  bg='white' marginBlock='5px'>
              <Text fontSize='lg' fontWeight='500'>Password</Text>
              <InputGroup>
                <Input variant='outline' placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} type={showPassword ? "text" : "password"}/>
                <InputRightElement w={"max-content"} height='100%'>
                  {showPassword ? <IconButton variant={"ghost"} onClick={() => setShowPassword(!showPassword)} aria-label="Hidden-Password" icon={<Icon as={AiFillEye}/>}/> : 
                    <IconButton variant={"ghost"} onClick={() => setShowPassword(!showPassword)} aria-label="Hidden-Password" icon={<Icon as={AiFillEyeInvisible}/>}/>}
                </InputRightElement>
              </InputGroup>
            </Box>
        
            <Button type="submit" alignSelf={"flex-start"} name="login" role="button" data-testid="login" >Login</Button>
        
            <Link w='fit-content' href="/signup">
        New user? Create an account. <ExternalLinkIcon mx='2px' mb='2px' />
            </Link>
          </VStack>
        </form>
      </Center>
    </Container>
  );
}

export default withUnauthenticated(Login);
