/**
 * This file contains the Profile component of the application.
 * The Profile component is a React component that displays the profile page of the current user.
 * It fetches the current user's data and the studies associated with the user, and displays them in a user-friendly format.
 * It also provides a feature for the user to copy their unique ID to the clipboard.
 */

// Import necessary libraries, components, hooks, and types.
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import {
  Box,
  VStack,
  Flex,
  Divider,
  chakra,
  Grid,
  GridItem,
  Container,
  Heading,
  Link,
  Text,
  Icon,
  IconButton
} from "@chakra-ui/react";
import { fetchStudies } from "@/data";
import { Study } from "@/data/types";
import { useState, useEffect, useMemo, useCallback } from "react";

import NextLink from "next/link";
import { FiCopy } from "react-icons/fi/index.js";

/**
 * The Profile component is a React component that displays the profile page of the current user.
 * It fetches the current user's data and the studies associated with the user, and displays them in a user-friendly format.
 * It also provides a feature for the user to copy their unique ID to the clipboard.
 */
function Profile() {
  // Fetch the current user's data and the studies associated with the user.
  const { currentUser } = useAuthContext();
  const [studies, setStudies] = useState<Study[]>([]);
  const [copied, setCopied] = useState(false);

  // Reverse the studies array for display purposes.
  const reversedStudies = useMemo(() => studies.slice().reverse(), [studies]);

  // Fetch the studies data when the component mounts.
  useEffect(() => {
    async function loadStudies() {
      const data = await fetchStudies();
      if (data) {
        setStudies(data);
      }
    }
    loadStudies();
  }, []);

  // Determine if the current user is a customer.
  const isCustomer = currentUser?.role === "customer";

  // Handle the copy ID button click event.
  const onCopyId = useCallback(() => {
    if (!currentUser) return;
    navigator.clipboard.writeText(currentUser.id.toString());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [currentUser]);

  return (
    <Box as={Container} maxW="7xl" mt={14} p={4}>
      <Grid
        templateColumns={{
          base: "repeat(1, 1fr)",
          sm: "repeat(2, 1fr)",
          md: "repeat(2, 1fr)"
        }}
        gap={4}
      >
        <GridItem colSpan={1}>
          <Box
            height={"full"}
            p="50"
            w="100%"
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
          >
            <VStack
              position={"relative"}
              alignItems="flex-start"
              spacing="20px"
            >
              <Heading fontSize="6xl" fontWeight="700" color="black">
                {currentUser?.first_name} {currentUser?.last_name}
              </Heading>
              <Heading fontSize="3xl" fontWeight="700" color="blue.400">
                {currentUser?.email}
              </Heading>
              <Heading
                data-testid="role"
                fontSize="3xl"
                fontWeight="700"
                color="red.400"
              >
                {currentUser?.role}{" "}
                {isCustomer ? `(id: #${currentUser.id})` : ""}
              </Heading>

              {isCustomer &&
                (copied ? (
                  <Text fontSize="sm" color="green.500">
                    Copied to clipboard!
                  </Text>
                ) : (
                  <Flex gap={1} color={"gray"} alignItems={"baseline"}>
                    <Text fontSize="sm">
                      Copy and share your unique ID with your provider to use
                      their services.
                    </Text>
                    <IconButton
                      data-testid="copy-id-button"
                      icon={<Icon onClick={onCopyId} as={FiCopy} />}
                      aria-label={"copy-id-button"}
                      variant={"ghost"}
                      m={0}
                      p={0}
                      minH={0}
                      minW={0}
                      h={0}
                    />
                  </Flex>
                ))}
            </VStack>
          </Box>
        </GridItem>
        <GridItem>
          <Flex height={"full"}>
            <Box
              p="50"
              alignItems="centered"
              w="100%"
              borderWidth="1px"
              borderRadius="lg"
              overflow="hidden"
            >
              <VStack alignItems="center" spacing="10px">
                <Heading fontSize="xl">
                  At BotImage, we strive to provide a fully extensible and
                  scalable solution to even the most complex studies. As a valued
                  customer, you have used our site to track
                </Heading>
                <Heading
                  alignItems="centered"
                  p="10"
                  fontSize="5xl"
                  fontWeight="700"
                  fontStyle="bold"
                  color="purple.500"
                >
                  {studies.length} studies
                </Heading>
              </VStack>
            </Box>
          </Flex>
        </GridItem>
      </Grid>
      <Divider mt={12} mb={12} />
      <Heading fontSize={"3xl"} py="5">
        Recent Studies
      </Heading>
      <Flex
        direction={{ base: "column", md: "row" }}
        gap={{ base: "2", sm: "4", md: "8" }}
      >
        {reversedStudies.length === 0 && (
          <Text fontSize={"1xl"} textAlign={"center"}>
            No studies found.
          </Text>
        )}
        {reversedStudies.slice(0, 4).map((study) => (
          <Box
            key={study.id}
            p="10"
            w="100%"
            height="100%"
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
          >
            <Heading>{study.study_configuration.name} </Heading>
            <Text>#{study.id}</Text>
            <chakra.p>
              See this study{" "}
              <Link as={NextLink} href={`/studies/${study.id}`} color="blue.500">
                here
              </Link>
            </chakra.p>
          </Box>
        ))}
      </Flex>
    </Box>
  );
}

/**
 * Export the Profile component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Profile);
