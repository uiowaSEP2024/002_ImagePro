/**
 * This file contains the SignUp component of the application.
 * The SignUp component is a React component that provides a sign-up form for the user.
 * It fetches the user's input, validates it, and attempts to create a new user account.
 * It also provides feedback to the user in the form of error or success messages.
 */

// Import necessary libraries, components, hooks, and types.
import React, { FormEvent, useCallback, useState, useEffect } from "react";
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
  Flex,
    Select
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai/index.js";
import { useAuthContext } from "@/hooks/useAuthContext";
import { fetchSignUp } from "@/data";
import { withUnauthenticated } from "@/components/withAuthenticated";
import { User } from "@/data/types";

import NextLink from "next/link";

/**
 * The SignUp component is a React component that provides a sign-up form for the user.
 * It fetches the user's input, validates it, and attempts to create a new user account.
 * It also provides feedback to the user in the form of error or success messages.
 */
function SignUp() {
  // Initialize state variables for the sign-up form fields and error/success messages.
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [notificationMessage, setNotificationMessage] = useState("");
  const [role, setRole] = useState<User["role"]>("hospital");
  const [hospitals, setHospitals] = useState([]); // State to store fetched hospitals
  const [selectedHospital, setSelectedHospital] = useState(""); // State to store the selected hospital
  const [providers, setProviders] = useState([]); // State to store fetched providers
  const [selectedProvider, setSelectedProvider] = useState(""); // State to store the selected provider
  // Fetch the logIn function from the authentication context.
  const { logIn } = useAuthContext();

  // Fetch the list of hospitals from the database
  useEffect(() => {
    const fetchHospitals = async () => {
      try {
        const response = await fetch("/api/hospitals"); // Adjust this to your API endpoint
        const data = await response.json();
        setHospitals(data.hospitals); // Adjust this based on your API response structure
      } catch (error) {
        console.error("Failed to fetch hospitals:", error);
        setErrorMessage("Failed to load hospitals.");
      }
    };

    const fetchProviders = async () => {
      try {
        const response = await fetch("/api/providers"); // Adjust this to your API endpoint
        const data = await response.json();
        setProviders(data.providers); // Adjust this based on your API response structure
      } catch (error) {
        console.error("Failed to fetch providers:", error);
        setErrorMessage("Failed to load providers.");
      }
    };

    fetchProviders();
    fetchHospitals();

  }, []);


  // Define the sign-up request function.
  const sendSignUpReq = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();

      // Validate the user's input.
      if (confirmPassword !== password) {
        console.log("Passwords Do Not Match");
        setErrorMessage("Passwords Do Not Match");
        return;
      }

      // Attempt to create a new user account.
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





  // Render the SignUp component.
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
              <Radio value="hospital">Hospital</Radio>
              <Radio value="provider">Provider</Radio>
            </Stack>
          </RadioGroup>

           {/* Conditional Dropdown based on selected role */}
          {role === "hospital" ? (
            <Box flex="1" w="100%">
              <Text fontSize="md" fontWeight="medium">Select Hospital</Text>
              <Select
                placeholder="Select hospital"
                onChange={(e) => setSelectedHospital(e.target.value)}
                value={selectedHospital}
              >
                {hospitals.map((hospital) => (
                  <option key={hospital.id} value={hospital.id}>{hospital.hospital_name}</option>
                ))}
              </Select>
            </Box>
          ) : role === "provider" ? (
            <Box flex="1" w="100%">
              <Text fontSize="md" fontWeight="medium">Select Provider</Text>
              <Select
                placeholder="Select provider"
                onChange={(e) => setSelectedProvider(e.target.value)}
                value={selectedProvider}
              >
                {providers.map((provider) => (
                  <option key={provider.id} value={provider.id}>{provider.provider_name}</option>
                ))}
              </Select>
            </Box>
          ) : null}

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

/**
 * Export the SignUp component wrapped with the withUnauthenticated higher-order component.
 */
export default withUnauthenticated(SignUp);
