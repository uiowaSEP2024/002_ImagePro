import { fetchAPIkeys } from "@/data";
import { Key } from "@/data/types";
import React, { useRef } from "react";
import { useState, useEffect } from "react";
import {
    Heading,
    Text,
    Grid,
    GridItem,
    Card,
    CardBody,
    Spacer,
    Input,
    Button,
    Container,
    AlertDialog,
    AlertDialogBody,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogContent,
    AlertDialogOverlay,
    useDisclosure,
} from "@chakra-ui/react"
import { FocusableElement } from '@chakra-ui/utils'
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";

export default function ApiKeys() {
    const { currentUser } = useAuthContext()
    const [note, setNote] = useState("");
    const [keys, setKeys] = useState<Key[]>([]);
    const [firstKeys, setFirstKeys] = useState<Key[]>([])
    const [isOpen, setIsOpen] = useState(false);
    const cancelRef = React.useRef(null)

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
                if (data) setFirstKeys(data)
                setIsOpen(true)
            })
            .catch((e) => {
                console.log(e)
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
                        Manage API Keys for your provider account
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
            <AlertDialog
                isOpen={isOpen}
                leastDestructiveRef={cancelRef}
                onClose={() => {
                    setIsOpen(false);
                }}
                isCentered
                motionPreset="slideInBottom"
            >
                <AlertDialogOverlay>
                    <AlertDialogContent>
                        <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                            API Key 
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            Please copy this key for later. This is the only time you will see it.
                        </AlertDialogBody>
                        <AlertDialogFooter>
                            <Button ref={cancelRef} onClick={() => {
                                setIsOpen(false);
                            }}>
                                Ok
                            </Button>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog>
        </Container>
    );
}