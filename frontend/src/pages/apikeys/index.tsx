import { fetchAPIkeys, Key } from "@/data";
import React from "react";
import { useState, useEffect } from "react";
import { Text } from "@nextui-org/react";
import { Container, Row, Spacer, Input, Grid, Button, Card } from "@nextui-org/react";
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
      .then((data) => {
        // console.log(data)
        setNotificationMessage("API Keys Generated Successfully")
      })
      .catch((e) => {
        console.log(e)
        setNotificationMessage("Try again later!");
      })
  }
  return (
    <>
      {!!notificationMessage && <Text>{notificationMessage}</Text>}
      <Container gap={2} justify="center">
        <Row>
          <Text h1 align-items="center">
                        API Keys
          </Text>
        </Row>
        <Row>
          <Text align-items="center">
                        Manage your API keys on this page
          </Text>
        </Row>
        <Spacer y={1} />
        <Grid aria-label="Keys">
          {keys.map((card) => (
            <Grid key={card.id} data-testid="testkeys">
              <Card>
                <Card.Body aria-label="key">
                  <Text>{card.key}</Text>
                </Card.Body>
              </Card>
              <Spacer y={1} />
            </Grid>
          ))}
        </Grid>
        <Spacer y={2} />
        <Row>
          <Text align-items="center">
                        What is this token for?
          </Text>
        </Row>
        <Spacer y={1} />
        <Grid>
          <Input
            bordered
            size="lg"
            color="primary"
            labelPlaceholder="Note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            css={{ mb: "6px" }}
          />
        </Grid>
        <Spacer y={1} />
        <Button onPress={generateAPIKey}>Generate</Button>
      </Container>
    </>
  );
}