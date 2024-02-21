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

const NavLink = ({ children, link }: { children: ReactNode; link: string }) => (
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

const Navbar = () => {
  const { currentUser, logOut } = useAuthContext();

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
      to: "/jobs",
      name: "Jobs",
      id: "jobs",
      show: currentUser?.role === "provider"
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

  const linksRight = currentUser
    ? linksRightAuthenticated
    : linksRightUnauthenticated;

  const linksLeft = currentUser
    ? linksLeftAuthenticated
    : linksLeftUnauthenticated;

  const navBarColor = currentUser?.role == "provider" ? "gray.100" : undefined;

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
