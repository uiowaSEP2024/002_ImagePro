import { fetchAPIkeys } from "@/data";
import { Key } from "@/data/types";
import React from "react";
import { useState, useEffect } from "react";
import { Text } from '@chakra-ui/react'
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";

export default function ApiKeys() {
  const {currentUser} = useAuthContext()
  const [note, setNote] = useState("");
  const [notificationMessage, setNotificationMessage] = useState("");
  const [keys, setKeys] = useState<Key[]>([]);

  useEnsureAuthenticated()


  useEffect(() => {

    async function loadKeys() {
      const data = await fetchAPIkeys();
      if (data) setKeys(data);
    }

    console.log({currentUser})

    // if (currentUser){
    loadKeys() // TODO: wrap this back in check for currentUser
    // }

  }, [currentUser]);



  const generateAPIKey = () => {
    fetch("http://localhost:8000/api-keys", {
      credentials: "include",
      method: "POST"
    })
      .then((response) => response.json())
      .then(() => {
        setNotificationMessage("API Keys Generated Successfully")
      })
      .catch((e) => {
        console.log(e)
        setNotificationMessage("Try again later!");
      })
  }
  return (
    <Text fontSize='45px'>
        Generate API Keys
    </Text>
  );
}