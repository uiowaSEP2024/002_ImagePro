import React, { FormEvent, useCallback, useState } from "react";
import { MdErrorOutline } from "react-icons/md/index.js";
import ErrorMessageBox from "@/components/ErrorMessageBox";
import {
  Text,
  Container,
  VStack,
  Box,
  Input,
  Button,
  InputGroup,
  InputRightElement,
  Icon,
  IconButton,
  Link,
  RadioGroup,
  Radio,
  Stack,
  Heading,
  Flex
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai";
import { useAuthContext } from "@/hooks/useAuthContext";
import { fetchSignUp } from "@/data";
import { withUnauthenticated } from "@/components/withAuthenticated";
import { User } from "@/data/types";

import NextLink from "next/link";

function SignUp() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [errorMessage, setErrorMessage] = useState("");
  const [notificationMessage, setNotificationMessage] = useState("");

  const [role, setRole] = useState<User["role"]>("customer");

  const { logIn } = useAuthContext();

  const sendSignUpReq = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();

      if (confirmPassword !== password) {
        console.log("Passwords Do Not Match");
        setErrorMessage("Passwords Do Not Match");
        return;
      }

      try {
        await fetchSignUp({
          email,
          first_name,
          last_name,
          password,
          role
        });
        setNotificationMessage("Sign up successful! Logging you in...");
        await logIn(email, password);
      } catch (e) {
        console.log(e);
        setErrorMessage("Sign up failed!");
      }
    },
    [confirmPassword, email, first_name, last_name, logIn, password, role]
  );

  return (
    <Container
      pt={"5vh"}
      display={"flex"}
      justifyContent={"center"}
      maxW={"md"}
      alignItems={"center"}
      flexDirection={"column"}
    >
      {!!notificationMessage && (
        <Text data-test-id="notification-message">{notificationMessage}</Text>
      )}
      {!!errorMessage && <ErrorMessageBox errorMessage={errorMessage} />}

      <Heading role="heading" fontSize="3xl" mb={8}>
        Sign up
      </Heading>

      <form style={{ width: "100%" }} onSubmit={sendSignUpReq}>
        <VStack alignItems={"flex-start"} spacing={4}>
          <Box flex="1" w="100%">
            <Text fontSize="md" fontWeight="medium">
              First Name
            </Text>
            <Input
              variant="outline"
              id="First Name"
              placeholder="First Name"
              value={first_name}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </Box>
          <Box flex="1" w="100%">
            <Text fontSize="md" fontWeight="medium">
              Last Name
            </Text>
            <Input
              variant="outline"
              id="Last Name"
              placeholder="Last Name"
              value={last_name}
              onChange={(e) => setLastName(e.target.value)}
            />
          </Box>
          <Box flex="1" w="100%">
            <Text fontSize="md" fontWeight="medium">
              Email
            </Text>
            <Input
              variant="outline"
              id="Email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Box>
          <Box flex={1} w={"100%"}>
            <Text fontSize="md" fontWeight="medium">
              Password
            </Text>
            <InputGroup>
              <Input
                variant="outline"
                placeholder="Password"
                id="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type={showPassword ? "text" : "password"}
              />
              <InputRightElement w={"max-content"} height="100%">
                {showPassword ? (
                  <IconButton
                    variant={"ghost"}
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Hidden-Password"
                    icon={<Icon as={AiFillEye} />}
                  />
                ) : (
                  <IconButton
                    variant={"ghost"}
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Hidden-Password"
                    icon={<Icon as={AiFillEyeInvisible} />}
                  />
                )}
              </InputRightElement>
            </InputGroup>
          </Box>
          <Box flex="1" w="100%">
            <Text fontSize="md" fontWeight="medium">
              Confirm Password
            </Text>
            <Input
              variant="outline"
              type="password"
              id="Confirm Password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </Box>

          <RadioGroup
            alignSelf={"flex-start"}
            onChange={(value) => setRole(value as User["role"])}
            value={role}
          >
            <Stack direction="row" gap={8}>
              <Radio value="customer">Customer</Radio>
              <Radio value="provider">Provider</Radio>
            </Stack>
          </RadioGroup>

          <Button
            type="submit"
            alignSelf={"flex-start"}
            name="signup"
            role="button"
            data-testid="signup"
          >
            Create Account
          </Button>

          <Link passHref as={NextLink} w="fit-content" href="/login">
            <Flex alignItems={"center"} gap={2}>
              <Text>Already have an account? Log in. </Text>

              <ExternalLinkIcon mx="2px" mb="2px" />
            </Flex>
          </Link>
        </VStack>
      </form>
    </Container>
  );
}

export default withUnauthenticated(SignUp);
