import { Navbar } from "@nextui-org/react";
import React from "react";

function TopNavbar() {
  return (
    <Navbar variant="sticky">
      <Navbar.Content activeColor="primary" enableCursorHighlight hideIn="xs" variant="underline">
        <Navbar.Link href="/">Home</Navbar.Link>
        <Navbar.Link href="/dashboard">Dashboard</Navbar.Link>
        <Navbar.Link href="/billing">Billing</Navbar.Link>
      </Navbar.Content>
      <Navbar.Content enableCursorHighlight hideIn="xs">
        <Navbar.Link href="/login">Login</Navbar.Link>
        <Navbar.Link href="/signup">Sign up</Navbar.Link>
      </Navbar.Content>
    </Navbar>
  );
}

export default TopNavbar;
