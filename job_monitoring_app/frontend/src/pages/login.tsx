/**
 * Importing necessary libraries, components and hooks.
 */
import React, { FormEvent } from "react";
import { useState } from "react";
import { useRouter } from "next/router";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai/index.js";
import ErrorMessageBox from "@/components/ErrorMessageBox";
import {
  Container,
  Icon,
  IconButton,
  Text,
  Box,
  Input,
  Button,
  InputGroup,
  InputRightElement,
  Link,
  VStack,
  Flex,
  Heading
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { useAuthContext } from "@/hooks/useAuthContext";
import { withUnauthenticated } from "@/components/withAuthenticated";
import NextLink from "next/link";

/**
 * Login component.
 * This component is responsible for rendering the login form and handling the login process.
 */
function Login() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [notificationMessage, setNotificationMessage] = useState("");

  const { logIn } = useAuthContext();

  /**
   * Handles the login process.
   * @param {FormEvent} e - The form event.
   */
  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const result = await logIn(email, password);
      if (result && result.user) {
        setNotificationMessage("Login successful. Redirecting...");
        router.push("/dashboard");
      }
    } catch (e) {
      console.log(e);
      setErrorMessage("Login failed. Please try again.");
    }
  };

  /**
   * Returns the JSX to render.
   */
  return (
    <Container
      pt={"15vh"}
      display={"flex"}
      justifyContent={"center"}
      maxW={"md"}
      alignItems={"center"}
      flexDirection={"column"}
    >
      {!!notificationMessage && <Text>{notificationMessage}</Text>}
      {!!errorMessage && <ErrorMessageBox errorMessage={errorMessage} />}
      <Heading role="heading" fontSize="3xl" mb={4}>
        Login
      </Heading>
      <form style={{ width: "100%" }} onSubmit={handleLogin}>
        <VStack align={"flex-start"} spacing={4}>
          <Box w={"100%"} flex={1} bg="white" marginBlock="5px">
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
          <Box flex={1} w={"100%"} bg="white" marginBlock="5px">
            <Text fontSize="md" fontWeight="medium">
              Password
            </Text>
            <InputGroup>
              <Input
                variant="outline"
                id="Password"
                placeholder="Password"
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
                    data-testid="showbutton"
                    variant={"ghost"}
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Hidden-Password"
                    icon={<Icon as={AiFillEyeInvisible} />}
                  />
                )}
              </InputRightElement>
            </InputGroup>
          </Box>

          <Button
            type="submit"
            alignSelf={"flex-start"}
            name="login"
            role="button"
            data-testid="login"
          >
            Login
          </Button>

          <Link passHref as={NextLink} href="/signup">
            <Flex alignItems={"center"} gap={2}>
              <Text>New user? Create an account.</Text>
              <ExternalLinkIcon bgSize={"sm"} />
            </Flex>
          </Link>
        </VStack>
      </form>
    </Container>
  );
}

/**
 * Exporting the Login component wrapped with the withUnauthenticated HOC.
 */
export default withUnauthenticated(Login);
