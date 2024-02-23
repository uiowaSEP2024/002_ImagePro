import {
  Center,
  Container,
  Flex,
  HStack,
  Heading,
  Link,
  Text
} from "@chakra-ui/react";
import React from "react";

import NextLink from "next/link";
import { useAuthContext } from "@/hooks/useAuthContext";

/**
 * Footer is a functional component that renders a footer.
 * The footer includes links to different pages of the application.
 * The links displayed in the footer depend on whether the user is authenticated.
 *
 * @returns {JSX.Element} The Footer component.
 */
const Footer = (): JSX.Element => {
  const { currentUser } = useAuthContext();

  // Define the links to be displayed in the footer.
  const links = [
    {
      to: "/",
      name: "Home",
      id: "home",
      show: true
    },
    {
      to: "/dashboard",
      name: "Dashboard",
      id: "dashboard",
      show: !!currentUser
    },
    {
      to: "/profile",
      name: "Profile",
      id: "profile",
      show: !!currentUser
    },
    {
      to: "/login",
      name: "Log in",
      id: "loginButton",
      show: !currentUser
    },
    {
      to: "/signup",
      name: "Sign up",
      id: "signup",
      show: !currentUser
    }
  ];

  // Render the Footer component.
  return (
    <Center mt={12} boxShadow={"xs"}>
      <Container py={4} maxW={"container.xl"} px={4}>
        <Flex
          direction={"column"}
          justifyContent={"center"}
          alignItems={"center"}
          gap={6}
        >
          <Link
            _hover={{ textDecoration: "none" }}
            passHref
            as={NextLink}
            href={"/"}
          >
            <Heading fontWeight={"extrabold"} fontSize={"2xl"}>
              tracker.com
            </Heading>
          </Link>
          <HStack spacing={4}>
            {links.map((link) =>
              link.show ? (
                <Link
                  key={link.id}
                  passHref
                  as={NextLink}
                  href={link.to}
                  fontWeight={"medium"}
                  _hover={{
                    textDecoration: "none"
                  }}
                >
                  {link.name}
                </Link>
              ) : null
            )}
          </HStack>

          <Text>©️ 2023 Tracker.com, All rights reserved.</Text>
        </Flex>
      </Container>
    </Center>
  );
};

export default Footer;
