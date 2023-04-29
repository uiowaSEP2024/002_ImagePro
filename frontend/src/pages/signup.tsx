import React, { FormEvent, useCallback, useState } from "react";
import {
  Text,
  Container,
  Center,
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
  Stack
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai";
import { useAuthContext } from "@/hooks/useAuthContext";
import { fetchSignUp } from "@/data";
import { withUnauthenticated } from "@/components/withAuthenticated";
import { User } from "@/data/types";

function SignUp() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [notificationMessage, setNotificationMessage] = useState("");

  const [role, setRole] = useState<User["role"]>("customer");

  const { logIn } = useAuthContext();

  const sendSignUpReq = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();

      if (confirmPassword !== password) {
        console.log("Passwords Do Not Match");
        setNotificationMessage("Passwords Do Not Match");
        return;
      }

      try {
        const data = await fetchSignUp({
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
        setNotificationMessage("Sign up failed!");
      }
    },
    [confirmPassword, email, first_name, last_name, logIn, password, role]
  );

  return (
    <Container
      display={"flex"}
      justifyContent={"center"}
      maxW={"container.lg"}
      py={"6"}
    >
      <Center
        maxW={"xs"}
        display="flex"
        flexDirection="column"
        paddingTop={"6vh"}
      >
        {!!notificationMessage && (
          <Text data-test-id="notification-message">{notificationMessage}</Text>
        )}
        <form onSubmit={sendSignUpReq}>
          <VStack spacing={4}>
            <Text role="heading" fontSize="36px" as="b">
              Sign up
            </Text>
            <Box flex="1" w="100%" bg="white">
              <Text fontSize="lg" fontWeight="500">
                First Name
              </Text>
              <Input
                variant="outline"
                placeholder="First Name"
                value={first_name}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </Box>
            <Box flex="1" w="100%" bg="white">
              <Text fontSize="lg" fontWeight="500">
                Last Name
              </Text>
              <Input
                variant="outline"
                placeholder="Last Name"
                value={last_name}
                onChange={(e) => setLastName(e.target.value)}
              />
            </Box>
            <Box flex="1" w="100%" bg="white">
              <Text fontSize="lg" fontWeight="500">
                Email
              </Text>
              <Input
                variant="outline"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Box>
            <Box flex={1} w={"100%"} bg="white">
              <Text fontSize="lg" fontWeight="500">
                Password
              </Text>
              <InputGroup>
                <Input
                  variant="outline"
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
                      variant={"ghost"}
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label="Hidden-Password"
                      icon={<Icon as={AiFillEyeInvisible} />}
                    />
                  )}
                </InputRightElement>
              </InputGroup>
            </Box>
            <Box flex="1" w="100%" bg="white">
              <Text fontSize="lg" fontWeight="500">
                Confirm Password
              </Text>
              <Input
                variant="outline"
                type="password"
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
            <Link w="fit-content" href="/login">
              Already have an account? Log in.{" "}
              <ExternalLinkIcon mx="2px" mb="2px" />
            </Link>
          </VStack>
        </form>
      </Center>
    </Container>
  );
}

export default withUnauthenticated(SignUp);
