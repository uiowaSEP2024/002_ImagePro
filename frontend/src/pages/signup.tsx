import React, { useState } from "react";


import { Flex, Text, Box, Input, InputGroup, Button, InputRightElement, Link } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons"
import { useAuthContext } from "@/hooks/useAuthContext";
import { fetchSignUp } from "@/data";
import { withUnauthenticated } from "@/components/withAuthenticated";

function SignUp() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  const { logIn } = useAuthContext()


  const sendSignUpReq = async () => {
    if (confirmPassword !== password) {
      console.log("Passwords Do Not Match");
      return;
    }

    try{
      const data = await fetchSignUp({
        email,
        first_name,
        last_name,
        password
      })
      console.log(data)
      setNotificationMessage("Sign up successful! Logging you in...");
      await logIn(email, password)
    }catch(e){
      console.log(e);
      setNotificationMessage("Sign up failed!");
    }
  };

  return (
    <Flex color='black' direction='column' padding='30px'>
      {!!notificationMessage && <Text data-test-id='notification-message'>{notificationMessage}</Text>}
      <Text fontSize='36px' as='b' marginBottom='10px'>Sign up</Text>
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>First Name</Text>
        <Input variant='filled' size='sm' placeholder="First Name" value={first_name} onChange={(e) => setFirstName(e.target.value)}/>
      </Box>
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>Last Name</Text>
        <Input variant='filled' size='sm' placeholder="Last Name" value={last_name} onChange={(e) => setLastName(e.target.value)}/>
      </Box>
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>Email</Text>
        <Input variant='filled' size='sm' placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
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
      <Box flex='1' w='200px' bg='white' marginBlock='5px'>
        <Text fontFamily='20px' fontWeight='500'>Confirm Password</Text>
        <Input variant='filled' size='sm' type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/>
      </Box>
      <Box flex='1' w='100px' marginBlock='10px'>
        <Button size='sm' name="signup" role="button" data-testid="signup" onClick={sendSignUpReq}>Create Account</Button>
      </Box>
      <Link href="/login">
        Already have an account? Log in. <ExternalLinkIcon mx='2px' mb='2px' />
      </Link>
    </Flex>
  );
}


export default withUnauthenticated(SignUp)
