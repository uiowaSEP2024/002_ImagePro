import { fetchAPIkeys, fetchGenAPIKeys } from "@/data";
import { ApiKey } from "@/data/types";
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
  Stack,
  VStack,
  Box
} from "@chakra-ui/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";

function ApiKeys() {
  const { currentUser } = useAuthContext();
  const [note, setNote] = useState("");
  const [keys, setKeys] = useState<ApiKey[]>([]);
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
    try {
      const data = await fetchGenAPIKeys({
        note
      });
      setFirstNote(data.note);
      setKey(data.key);
      onOpen();
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Container pt={12} maxW="container.lg">
      <Box mb={8}>
        <Heading>API Keys</Heading>
        <Text>Manage API Keys for your provider account</Text>
      </Box>

      <VStack alignItems={"flex-start"} spacing={8}>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendGenAPIKeyRequest();
            setNote("");
          }}
        >
          <Heading size={"lg"}>Create API Key</Heading>

          <Stack mt={4} maxWidth={"sm"} gap={2} direction={"column"}>
            <Input
              placeholder="Note"
              id="Note"
              size="lg"
              value={note}
              required
              onChange={(e) => setNote(e.target.value)}
            />

            <Button
              width={"fit-content"}
              type="submit"
              data-testid="submit"
              colorScheme="telegram"
            >
              Create Key
            </Button>
          </Stack>
        </form>

        <Box width={"full"}>
          <Heading pt={8} size={"lg"}>
            Existing Keys ({keys.length})
          </Heading>

          {reversedKeys.map((card) => (
            <Grid width={"full"} key={card.id} data-testid="testkeys">
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
        </Box>
      </VStack>

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
