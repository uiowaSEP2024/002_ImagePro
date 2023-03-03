import { Navbar } from "@nextui-org/react";

function TopNavbar() {
  return (
    <Navbar variant="sticky">
      <Navbar.Content enableCursorHighlight hideIn="xs">
        <Navbar.Link isActive href="/">
          Home
        </Navbar.Link>
        <Navbar.Link href="#">Dashboard</Navbar.Link>
        <Navbar.Link href="#">Billing</Navbar.Link>
      </Navbar.Content>
      <Navbar.Content enableCursorHighlight hideIn="xs">
        <Navbar.Link href="#">Login</Navbar.Link>
        <Navbar.Link isActive href="/signup">
          Sign up
        </Navbar.Link>
      </Navbar.Content>
    </Navbar>
  );
}

export default TopNavbar;
