import { fetchAPIkeys, fetchGenAPIKeys } from "@/data";
import { Key } from "@/data/types";
import React, { useCallback, useMemo } from "react";
import { useState, useEffect } from "react";
import {
  Heading,
  Text,
  Grid,
  GridItem,
  Card,
  CardBody,
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
  Stack
} from "@chakra-ui/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";

function ApiKeys() {
  const { currentUser } = useAuthContext();
  const [note, setNote] = useState("");
  const [keys, setKeys] = useState<Key[]>([]);
  const [key, setKey] = useState("");
  const [firstNote, setFirstNote] = useState("");
  const cancelRef = React.useRef(null);

  const { isOpen, onOpen, onClose } = useDisclosure();

  const reversedKeys = useMemo(() => keys.slice().reverse(), [keys]);

  const loadKeys = useCallback(async () => {
    const data = await fetchAPIkeys();
    if (data) setKeys(data);
  }, []);

  useEffect(() => {
    loadKeys();
  }, [currentUser, loadKeys]);

  const closeAlert = useCallback(() => {
    onClose();
    loadKeys();
  }, [loadKeys, onClose]);

  const sendGenAPIKeyRequest = async () => {
    try{
      const data = await fetchGenAPIKeys({
        note
      })
      setFirstNote(data.note);
      setKey(data.key);
      onOpen();
    }catch(e){
      console.log(e);
    }
  };

  return (
    <Container maxW="container.lg" py={"6"}>
      <Grid>
        <GridItem>
          <Heading>API Keys</Heading>
        </GridItem>
        <GridItem>
          <Text>Manage API Keys for your provider account</Text>
        </GridItem>

        <Heading pt={8} size={"lg"}>
          Create API Key
        </Heading>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendGenAPIKeyRequest();
            setNote("");
          }}
        >
          <Stack maxWidth={"sm"} gap={2} direction={"column"}>
            <Input
              placeholder="Note"
              size="lg"
              value={note}
              required
              onChange={(e) => setNote(e.target.value)}
            />

            <Button width={"fit-content"} type="submit" data-testid='submit' colorScheme="telegram">
              Create Key
            </Button>
          </Stack>
        </form>

        <Heading pt={8} size={"lg"}>
          Existing Keys ({keys.length})
        </Heading>

        <GridItem>
          {reversedKeys.map((card) => (
            <Grid key={card.id} data-testid="testkeys">
              <Card
                borderRadius={"none"}
                borderColor={"gray.300"}
                borderBottomWidth={1}
                boxShadow={"none"}
              >
                <CardBody aria-label="key">
                  <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                    <GridItem
                      display={"flex"}
                      flexDirection={"row"}
                      alignItems={"center"}
                      gap={2}
                    >
                      <Text mr={2} fontSize={"lg"}>
                        {card.note}
                      </Text>
                      <Text color={"gray.500"}>{card.key}</Text>
                    </GridItem>
                    {/* TODO: add support for removing api keys */}
                    {/* <GridItem colStart={3}>
                      <Button size="sm" variant="delete">
                        Remove
                      </Button>
                    </GridItem> */}
                  </Grid>
                </CardBody>
              </Card>
            </Grid>
          ))}
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
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Successfully created &quot;{firstNote}&quot;
            </AlertDialogHeader>
            <Grid>
              <AlertDialogBody>
                <GridItem>
                  Please copy this key for later. This is the only time you will
                  see it.
                </GridItem>
                <GridItem>
                  <Text as="b">{key}</Text>
                </GridItem>
              </AlertDialogBody>
            </Grid>
            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={closeAlert}>
                OK
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Container>
  );
}

export default withAuthenticated(ApiKeys, ["provider"]);
