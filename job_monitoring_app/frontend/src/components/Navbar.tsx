import { useAuthContext } from "@/hooks/useAuthContext";
import { ReactNode } from "react";
import {
  Button,
  Center,
  Container,
  Flex,
  HStack,
  Link
} from "@chakra-ui/react";
import React from "react";

import NextLink from "next/link";

/**
 * NavLink is a functional component that renders a navigation link.
 *
 * @param {object} props - The properties passed to the component.
 * @param {ReactNode} props.children - The child elements to be rendered within the link.
 * @param {string} props.link - The URL that the link points to.
 * @returns {JSX.Element} The NavLink component.
 */
const NavLink = ({ children, link }: { children: ReactNode; link: string }): JSX.Element => (
  <Link
    as={NextLink}
    px={4}
    py={2}
    rounded={"md"}
    _hover={{
      textDecoration: "none",
      bg: "gray.100"
    }}
    href={link}
    fontWeight={"bold"}
  >
    {children}
  </Link>
);

/**
 * Navbar is a functional component that renders a navigation bar.
 * The navigation bar includes links to different pages of the application.
 * The links displayed in the navigation bar depend on whether the user is authenticated and their role.
 *
 * @returns {JSX.Element} The Navbar component.
 */
const Navbar = (): JSX.Element => {
  const { currentUser, logOut } = useAuthContext();

  // Define the links to be displayed in the navigation bar when the user is not authenticated.
  const linksRightUnauthenticated = [
    {
      to: "/login",
      name: "Log in",
      id: "loginButton",
      show: true
    },
    {
      to: "/signup",
      name: "Sign up",
      id: "signup",
      show: true
    }
  ];

  const linksLeftUnauthenticated = [
    {
      to: "/",
      name: "Home",
      id: "home",
      show: true
    }
  ];

  // Define the links to be displayed in the navigation bar when the user is authenticated.
  const linksLeftAuthenticated = [
    {
      to: "/",
      name: "Home",
      id: "home",
      show: !!currentUser
    },
    {
      to: "/dashboard",
      name: "Dashboard",
      id: "dashboard",
      show: !!currentUser
    },
    {
      to: "/studies",
      name: "Studies",
      id: "studies",
      show: !!currentUser
    },
    {
      to: "/analytics",
      name: "Analytics",
      id: "analytics",
      show: currentUser?.role === "provider"
    },
    {
      to: "/reporting",
      name: "Reporting",
      id: "reporting",
      show: currentUser?.role === "provider"
    },
    {
      to: "/apikeys",
      name: "Generate API Keys",
      id: "apikeys",
      show: currentUser?.role === "provider"
    }
  ];

  const linksRightAuthenticated = [
    {
      to: "/profile",
      name: "My Profile",
      id: "profile",
      show: !!currentUser
    },
    {
      onClick: logOut,
      name: "Logout",
      id: "logoutButton",
      show: !!currentUser
    }
  ];

  // Determine which set of links to use based on whether the user is authenticated.
  const linksRight = currentUser
    ? linksRightAuthenticated
    : linksRightUnauthenticated;

  const linksLeft = currentUser
    ? linksLeftAuthenticated
    : linksLeftUnauthenticated;

  // Determine the color of the navigation bar based on the user's role.
  const navBarColor = currentUser?.role == "provider" ? "gray.100" : undefined;

  // Render the Navbar component.
  return (
    <Center bgColor={navBarColor} boxShadow={"xs"}>
      <Container py={2} maxW={"container.xl"} px={4}>
        <Flex alignItems={"center"} justifyContent={"space-between"}>
          <HStack as={"nav"} spacing={4} display={{ base: "none", md: "flex" }}>
            {linksLeft.map((link) => {
              if ("show" in link && !link.show) {
                return null;
              }
              return (
                <NavLink data-testid={link.id} key={link.name} link={link.to}>
                  {link.name}
                </NavLink>
              );
            })}
          </HStack>

          <HStack as={"nav"} spacing={2} display={{ base: "none", md: "flex" }}>
            {linksRight.map((link) => {
              if ("onClick" in link) {
                return (
                  <Button
                    data-testid={link.id}
                    key={link.name}
                    onClick={link.onClick}
                  >
                    {link.name}
                  </Button>
                );
              }

              return (
                <NavLink data-testid={link.id} key={link.name} link={link.to}>
                  {link.name}
                </NavLink>
              );
            })}
          </HStack>
        </Flex>
      </Container>
    </Center>
  );
};

export default Navbar;
