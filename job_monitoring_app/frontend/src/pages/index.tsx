/**
 * This file contains the Home component of the application.
 * The Home component is a React component that displays the home page of the application.
 * It fetches the current user's data and displays different features based on the user's authentication status.
 */

// Import necessary libraries, components, hooks, and types.
import { useAuthContext } from "@/hooks/useAuthContext";
import {
  Container,
  Stack,
  Flex,
  Heading,
  Text,
  Button,
  Image,
  Card
} from "@chakra-ui/react";
import { useRouter } from "next/router";

/**
 * The Home component is a React component that displays the home page of the application.
 * It fetches the current user's data and displays different features based on the user's authentication status.
 */
export default function Home() {
  // Fetch the current user's data and the router instance.
  const router = useRouter();
  const { currentUser } = useAuthContext();

  // Define the routes for the studies and analytics pages based on the user's authentication status.
  var studies = "studies";
  var analytics = "analytics";
  if (!currentUser) {
    studies = "login";
    analytics = "login";
  }

  // Render the Home component.
  return (
    <Container maxW={"7xl"}>
      <Stack
        align={"center"}
        spacing={{ base: 8, md: 10 }}
        py={{ base: 20, md: 28 }}
        direction={{ base: "column", md: "row" }}
      >
        <Stack flex={1} spacing={{ base: 5, md: 10 }}>
          <Heading
            lineHeight={1.1}
            fontWeight={600}
            fontSize={{ base: "3xl", sm: "4xl", lg: "6xl" }}
          >
            <Text as={"span"} position={"relative"} data-testid="header">
              Leave tracking
            </Text>
            <br />
            <Text as={"span"} color={"red.400"}>
              your progress to us
            </Text>
          </Heading>
          <Text color={"gray.500"}>
            Our solution to your study tracking problems! Our web app provides an
            interface for you to track the progress, analytics, and errors for
            all your studies and customers, no matter how many steps. Our app
            provides an easy API to add to your study scripts, which catalogues
            all your data and steps in a relational database stored securely by
            our AWS partners. From there, your data becomes easy to query and
            analyze. Never let a client slip through the cracks again!
          </Text>
          <Stack
            spacing={{ base: 4, sm: 6 }}
            direction={{ base: "column", sm: "row" }}
          >
            <Button
              onClick={() => router.push(studies)}
              size={"lg"}
              fontWeight={"normal"}
              px={6}
              colorScheme={"red"}
              bg={"red.400"}
              _hover={{ bg: "red.500" }}
            >
              Learn More About Studies
            </Button>
            <Button
              onClick={() => router.push(analytics)}
              size={"lg"}
              fontWeight={"normal"}
              bg={"#0072f5"}
              _hover={{ bg: "#0164d6" }}
              px={6}
            >
              Get Started With Analytics
            </Button>
          </Stack>
        </Stack>
        <Flex
          flex={1}
          justify={"center"}
          align={"center"}
          position={"relative"}
          w={"full"}
        >
          <Card
            position={"relative"}
            height={"300px"}
            boxShadow={"2xl"}
            rounded={"2xl"}
            width={"full"}
            overflow={"hidden"}
            borderWidth={"2px"}
            borderColor={"gray.50"}
          >
            <Image
              alt={"Studies Progress Page"}
              fit={"cover"}
              align={"center"}
              src={"/assets/studies.png"}
            />
          </Card>
        </Flex>
      </Stack>
    </Container>
  );
}
