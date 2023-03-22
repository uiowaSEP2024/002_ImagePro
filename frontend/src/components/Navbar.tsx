import { Navbar, Button } from "@nextui-org/react";
import React from "react";
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";

function TopNavbar() {
  const router = useRouter();
  const [data, setData] = useState(null)

  const sendLogOutReq = () => {
    fetch("http://localhost:8000/logout", {
      method: "POST",
      credentials: "include",
    }).then((data) => {
      router.push("/")
    })
  }

  useEffect(() => {
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }
    ).then((result) => result.json()).then((data) => {
      setData(data.detail)
      console.log(data.detail)
    })
  })
  if (data == "Not authenticated") {
    return (
      <Navbar variant="sticky">
        <Navbar.Content activeColor="primary" enableCursorHighlight hideIn="xs" variant="underline">
          <Navbar.Link href="/">Home</Navbar.Link>
        </Navbar.Content>
        <Navbar.Content enableCursorHighlight hideIn="xs">
          <Navbar.Link href="/login">Login</Navbar.Link>
          <Navbar.Link href="/signup">Sign up</Navbar.Link>
        </Navbar.Content>
      </Navbar>
    );
  }
  else {
    return (
      <Navbar variant="sticky">
        <Navbar.Content activeColor="primary" enableCursorHighlight hideIn="xs" variant="underline">
          <Navbar.Link href="/">Home</Navbar.Link>
          <Navbar.Link href="/dashboard">Dashboard</Navbar.Link>
          <Navbar.Link href="/billing">Billing</Navbar.Link>
        </Navbar.Content>
        <Navbar.Content enableCursorHighlight hideIn="xs">
        <Button flat light color="default" onPress={sendLogOutReq}>Log Out</Button>
        </Navbar.Content>
      </Navbar>
    );
  }
}

export default TopNavbar;