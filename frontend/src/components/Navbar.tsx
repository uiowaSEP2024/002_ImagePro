import { useAuthContext } from "@/hooks/useAuthContext";
import { ReactNode } from "react";
import { Button } from "@nextui-org/react";
import {
  Box,
  Flex,
  HStack,
  Link,
  useColorModeValue,
} from "@chakra-ui/react";
import React from "react";


const TopNavbar = () => {
  const { currentUser, logOut} = useAuthContext()

  const NavLink = ({ children, link }: { children: ReactNode, link: string }) => (
    <Link
      px={2}
      py={1}
      rounded={"md"}
      _hover={{
        textDecoration: "none",
        bg: useColorModeValue("gray.200", "gray.700"),
      }}
      href={link}>
      {children}
    </Link>
  )

  const links = [
    {
      to: "/login",
      name: "Log in",
      id: "loginButton"
    },
    {
      to: "/signup",
      name: "Sign up",
      id: "signup"
    }]

  const authenticatedLinks = [ 
    {
      to: "/",
      name: "Home"
    },
    {
      to: "/dashboard",
      name: "Dashboard"
    },
    {
      to: "/billing",
      name: "Billing"
    },
    {
      to: "/apikeys",
      name: "Generate API Keys"
    }]

  if (!currentUser) {
    return (
      <>
        <Box bg={"gray.100"} px={4}>
          <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
            <HStack spacing={8} alignItems={"center"}>
              <HStack
                as={"nav"}
                spacing={4}
                display={{ base: "none", md: "flex" }}>
                <NavLink link={"/"}>Home</NavLink>
              </HStack>
            </HStack>

            <Flex alignItems={"center"}>
              <HStack spacing={8} alignItems={"center"}>
                <HStack
                  as={"nav"}
                  spacing={4}
                  display={{ base: "none", md: "flex" }}>
                  {links.map(link => (<NavLink data-testid={link.id} key={link.name} link={link.to}> {link.name} </NavLink> ))}
                </HStack>
              </HStack>
            </Flex>
          </Flex>
        </Box>
      </>
    );
  }
  return (
    <>
      <Box bg={"gray.100"} px={4}>
        <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
          <HStack spacing={8} alignItems={"center"}>
            <HStack
              as={"nav"}
              spacing={4}
              display={{ base: "none", md: "flex" }}>
              {authenticatedLinks.map(link => (<NavLink key={link.name} link={link.to}> {link.name} </NavLink> ))}
            </HStack>
          </HStack>

          <Flex alignItems={"center"}>
            <HStack spacing={8} alignItems={"center"}>
              <HStack
                as={"nav"}
                spacing={4}
                display={{ base: "none", md: "flex" }}>
                <NavLink link={"/profile"}>My Profile</NavLink>
                <Button  data-testid="logoutButton" onPress={logOut}>Logout</Button>
              </HStack>
            </HStack>
          </Flex>
        </Flex>
      </Box>
    </>
  );
    
}

export default TopNavbar;