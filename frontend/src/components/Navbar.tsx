import { Navbar, Button } from "@nextui-org/react";
import React from "react";
import { useState, useEffect } from 'react';
import { useRouter } from "next/router";
import { checkUserLoggedIn } from "@/utils/auth";


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
    checkUserLoggedIn().then((data) => {
      setData(data.detail)
    }).catch((error) => {
      router.push('/login')
      console.log(error)
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
        <Navbar.Link href="/profile">My Profile</Navbar.Link>
        <Button flat light color="default" onPress={sendLogOutReq}>Log Out</Button>
        </Navbar.Content>
      </Navbar>
    );
  }
}

export default TopNavbar;