import { fetchAPIkeys } from "@/data";
import { Key } from "@/data/types";
import React from "react";
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
} from "@chakra-ui/react"
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";

export default function ApiKeys() {
    const { currentUser } = useAuthContext()
    const [note, setNote] = useState("");
    const [keys, setKeys] = useState<Key[]>([]);
    const [key, setKey] = useState("");
    const [firstnote, setFirstNote] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const cancelRef = React.useRef(null)

    useEnsureAuthenticated()


    useEffect(() => {

        async function loadKeys() {
            const data = await fetchAPIkeys();
            console.log(data)
            if (data) setKeys(data);
            console.log(data)
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
                setFirstNote(data.note)
                setKey(data.key)
                setIsOpen(true)
            })
            .catch((e) => {
                console.log(e)
            })
    }

    const closeAlert = () => {
        setIsOpen(false);
        window.location.reload();
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
                                    <Grid templateColumns='repeat(3, 1fr)' gap={4}>
                                        <GridItem colSpan={2} h='10'>{card.note}{card.key}</GridItem>
                                        <GridItem colStart={4} colEnd={3}><Button size='md' height='10' width='150px' border='2px' variant="delete" >Remove</Button></GridItem>
                                    </Grid>
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
                onClose={closeAlert}
                isCentered
                motionPreset="slideInBottom"
            >
                <AlertDialogOverlay>
                    <AlertDialogContent>
                        <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                            Successfully created &quot;{firstnote}&quot;
                        </AlertDialogHeader>
                        <Grid>

                            <AlertDialogBody>
                                <GridItem>
                                    Please copy this key for later. This is the only time you will see it.
                                </GridItem>
                                <GridItem>
                                    <Text as='b'>{key}</Text>
                                </GridItem>
                            </AlertDialogBody>
                        </Grid>
                        <AlertDialogFooter>
                            <Button ref={cancelRef} onClick={closeAlert}>
                                Ok
                            </Button>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog>
        </Container>
    );
}