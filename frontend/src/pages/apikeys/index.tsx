import { fetchAPIkeys } from "@/data";
import { Key } from "@/data/types";
import React from "react";
import { useState, useEffect } from "react";
import { Heading, Text, Grid, GridItem, Card, CardBody, Spacer, Input, Button, Container } from "@chakra-ui/react"
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";

export default function ApiKeys() {
    const { currentUser } = useAuthContext()
    const [note, setNote] = useState("");
    const [notificationMessage, setNotificationMessage] = useState("");
    const [keys, setKeys] = useState<Key[]>([]);

    useEnsureAuthenticated()


    useEffect(() => {

        async function loadKeys() {
            const data = await fetchAPIkeys();
            console.log(data)
            if (data) setKeys(data);
        }

        console.log({ currentUser })

        // if (currentUser){
        loadKeys() // TODO: wrap this back in check for currentUser
        // }

    }, [currentUser]);



    const generateAPIKey = () => {
        fetch("http://localhost:8000/api-keys", {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                note: note
            })
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                setNotificationMessage("API Keys Generated Successfully")
            })
            .catch((e) => {
                console.log(e)
                setNotificationMessage("Try again later!");
            })
    }


    return (
        <Container maxW="container.lg" py={"6"}>
            <Grid>
                <GridItem>
                    <Heading>
                        API Keys
                    </Heading>
                </GridItem>
                <GridItem>
                    <Text>
                        Manage API Keys for yout provider account
                    </Text>
                </GridItem>
                <Spacer height="30px" />
                <GridItem>
                    {keys.map((card) => (
                        <Grid key={card.id} data-testid="testkeys">
                            <Card>
                                <CardBody aria-label="key">
                                    <Text>{card.note}</Text>
                                </CardBody>
                            </Card>
                            <Spacer height="30px" />
                        </Grid>

                    ))}
                </GridItem>
                <Spacer height="50px" />
                <GridItem>
                    <Input placeholder="Note" size='lg' width='300px' value={note} onChange={(e) => setNote(e.target.value)} />
                </GridItem>
                <Spacer height="30px" />
                <GridItem>
                    <Button colorScheme='telegram' onClick={generateAPIKey}>Create Key</Button>
                </GridItem>
            </Grid>
        </Container>

    );
}