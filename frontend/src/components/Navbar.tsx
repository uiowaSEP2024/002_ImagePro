import { useAuthContext } from "@/hooks/useAuthContext";
import { ReactNode } from 'react';
import { Button } from "@nextui-org/react";
import {
  Box,
  Flex,
  HStack,
  Link,
  useDisclosure,
  useColorModeValue,
} from '@chakra-ui/react';
import React from "react";


const TopNavbar = () => {
  const { currentUser, logOut} = useAuthContext()

  const NavLink = ({ children, link }: { children: ReactNode, link: string }) => (
    <Link
      px={2}
      py={1}
      rounded={'md'}
      _hover={{
        textDecoration: 'none',
        bg: useColorModeValue('gray.200', 'gray.700'),
      }}
      href={link}>
      {children}
    </Link>
  )

  const { isOpen, onOpen, onClose } = useDisclosure();

  if (!currentUser) {
    return (
      <>
        <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4}>
          <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
            <HStack spacing={8} alignItems={'center'}>
              <HStack
                as={'nav'}
                spacing={4}
                display={{ base: 'none', md: 'flex' }}>
                  <NavLink link={'/'}>Home</NavLink>
              </HStack>
            </HStack>

          <Flex alignItems={'center'}>
            <HStack spacing={8} alignItems={'center'}>
              <HStack
                as={'nav'}
                spacing={4}
                display={{ base: 'none', md: 'flex' }}>
                  <NavLink data-testid="loginButton" link={'/login'}>Login</NavLink>
                  <NavLink link={'/signup'}>Sign up</NavLink>
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
      <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4}>
        <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
          <HStack spacing={8} alignItems={'center'}>
            <HStack
              as={'nav'}
              spacing={4}
              display={{ base: 'none', md: 'flex' }}>
                <NavLink link={'/'}>Home</NavLink>
                <NavLink link={'/dashboard'}>Dashboard</NavLink>
                <NavLink link={'/billing'}>Billing</NavLink>
                <NavLink link={'/apikeys'}>Generate API Keys</NavLink>
            </HStack>
          </HStack>

        <Flex alignItems={'center'}>
          <HStack spacing={8} alignItems={'center'}>
            <HStack
              as={'nav'}
              spacing={4}
              display={{ base: 'none', md: 'flex' }}>
                <NavLink link={'/profile'}>My Profile</NavLink>
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