import { useAuthContext } from "@/hooks/useAuthContext";
import { Navbar, Button } from "@nextui-org/react";
import React from "react";


const TopNavbar = () => {
  const { currentUser, logOut} = useAuthContext()

  if (!currentUser) {
    return (
      <Navbar variant="sticky">
        <Navbar.Content
          activeColor="primary"
          enableCursorHighlight
          hideIn="xs"
          variant="underline"
        >
          <Navbar.Link href="/">Home</Navbar.Link>
        </Navbar.Content>
        <Navbar.Content enableCursorHighlight hideIn="xs">
          <Navbar.Link href="/login">Login</Navbar.Link>
          <Navbar.Link href="/signup">Sign up</Navbar.Link>
        </Navbar.Content>
      </Navbar>
    )}

  return (
    <Navbar variant="sticky">
      <Navbar.Content
        activeColor="primary"
        enableCursorHighlight
        hideIn="xs"
        variant="underline"
      >
        <Navbar.Link href="/">Home</Navbar.Link>
        <Navbar.Link href="/dashboard">Dashboard</Navbar.Link>
        <Navbar.Link href="/billing">Billing</Navbar.Link>
        <Navbar.Link href="/apikeys">Generate API Keys</Navbar.Link>
      </Navbar.Content>
      <Navbar.Content enableCursorHighlight hideIn="xs">
        <Navbar.Link href="/profile">My Profile</Navbar.Link>
        <Button flat light color="default" data-testid="logoutButton" name="logoutButton" onPress={logOut}>
            Log Out
        </Button>
      </Navbar.Content>
    </Navbar>
  )
}

export default TopNavbar;
