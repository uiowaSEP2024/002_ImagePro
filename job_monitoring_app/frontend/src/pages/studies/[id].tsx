/**
 * This file contains the StudyPage component of the application.
 * The StudyPage component is a React component that displays the details of a specific study.
 * It fetches the study data and the events associated with the study from the server, and displays them in a user-friendly format.
 * The study details include the study's name, date, time, hospital ID, and provider.
 * The events are displayed in a timeline format, with each event represented by a timeline item.
 * The component also provides a feature for the user to report an issue with the study by sending an email to the system administrator.
 */

// Import necessary libraries, components, hooks, and types.
import { Metadata } from "@/components/Metadata";
import { EventTimeline } from "@/components/EventTimeline";
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchEvents, fetchStudyById } from "@/data";
import { Study, StudyEvent } from "@/data/types";
import { useEnsureAuthenticated } from "@/hooks/useAuthContext";
import { ArrowBackIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  VStack,
  Heading,
  Progress,
  Tooltip,
  Divider,
  Link,
  Box,
  Text,
  Spinner,
  Center,
  ThemingProps
} from "@chakra-ui/react";
import { useRouter } from "next/router";
import { useEffect, useMemo, useState } from "react";

// Define the type for the StudyEventWithNumber interface.
type StudyEventWithNumber = StudyEvent & { event_number: number };
// Define the type for event kinds
type Kind = "error" | "pending" | "complete" | "in_progress" | "info";


/**
 * The StudyPage component is a React component that displays the details of a specific study.
 * It fetches the study data and the events associated with the study from the server, and displays them in a user-friendly format.
 * The study details include the study's name, date, time, hospital ID, and provider.
 * The events are displayed in a timeline format, with each event represented by a timeline item.
 * The component also provides a feature for the user to report an issue with the study by sending an email to the system administrator.
 */
function StudyPage({ initialIsPageLoading = true }) {
  useEnsureAuthenticated();
  const router = useRouter();
  const { id: studyId } = router.query;
  const [events, setEvents] = useState<StudyEventWithNumber[]>([]);
  const [study, setStudy] = useState<Study | null>(null);
  const [isPageLoading, setIsPageLoading] = useState(initialIsPageLoading);

  const allEvents = useMemo(() => {
    return events.slice().sort((a, b) => a.id - b.id);
  }, [events]);

  const numSteps = useMemo(
    () => study?.study_configuration?.step_configurations.length,
    [study]
  );

  useEffect(() => {
    async function loadStudy() {
      const data = await fetchStudyById(studyId as unknown as number);
      if (data) setStudy(data);
    }

    if (studyId) {
      loadStudy();
    }
  }, [studyId]);

  // Derive the studyStatus based on the last event
  // If any event is an error, the study is in an error state
  // Otherwise, check if the study has a complete event
  const studyStatus = useMemo(() => {

    const hasErrorEvent = events.some((event) => event.kind === "Error");
    if (hasErrorEvent) {
      return "error";
    }

    const hasCompleteEvent = events.some((event) => event.kind === "Complete");
    return hasCompleteEvent ? "success" : "pending";
  }, [events]);

  useEffect(() => {
    const loadStudyEvents = async () => {
      try {
        const data = await fetchEvents(studyId as unknown as number);
        if (!data) {
          return true;
        }

        setEvents(
          data.map((event, index) => ({ ...event, event_number: index + 1 }))
        );

      } catch (e) {
        console.log(e);
      }

      setIsPageLoading(false);
    };

    const interval = setInterval(async () => {
      await loadStudyEvents();
      if (studyStatus === "success") {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [study, studyId, studyStatus, events]);

  // Derive the progress percentage based on numSteps and event kind
  // if it is available, or do 0 -> 1 -> 50 -> 100 based on the presence of any events
  const progressAmount = useMemo(() => {
    if (numSteps) {
      const stepEvents = events.filter((event) => !!event.step_configuration && (event.kind === "Complete" || event.kind === "Error"));
      return ((stepEvents.length / numSteps) * 100).toFixed(0);
    }

    if (studyStatus === "success") {
      return 100;
    }

    if (events.length) {
      return 50;
    }

    return 1;
  }, [numSteps, studyStatus, events]);

  // Derive the color of the progress bar based on computed study status
  const progressColorScheme = useMemo((): ThemingProps["colorScheme"] => {
    if (studyStatus === "error") {
      return "red";
    }

    return "whatsapp";
  }, [studyStatus]);

  // Don't show page until we have attempted to load some events
  if (isPageLoading) {
    return (
      <Container alignItems={"center"} maxW="container.lg" py={"6"}>
        <Center>
          <Spinner />
        </Center>
      </Container>
    );
  }

  const studyDate = study?.created_at ? new Date(study?.created_at) : null;

  const studyDetails = {
    "Study Name": study?.study_configuration.name,
    Date: studyDate ? studyDate.toLocaleDateString() : "-",
    Time: studyDate ? studyDate.toLocaleTimeString() : "-",
    "Hospital ID": study?.hospital_id,
    Provider: study?.provider.provider_name
  };

  return (
    <>
      <Container maxW="container.lg" py={"6"}>
        <VStack gap={"4"} w={"full"} align="left">
          <Link data-testid="backlink" href={"/studies"}>
            <Button
              size={"md"}
              fontWeight={"semibold"}
              variant={"link"}
              _hover={{}}
              data-testid="backarrow"
              leftIcon={<ArrowBackIcon />}
            >
              Back to Studies
            </Button>
          </Link>

          <Tooltip label={`${progressAmount}% complete`}>
            <Progress
              borderRadius={"xl"}
              isAnimated={Number(progressAmount) < 100}
              size="md"
              data-testid="progressFull"
              hasStripe={Number(progressAmount) < 100}
              colorScheme={progressColorScheme}
              value={Number(progressAmount)}
              sx={{
                "& > div:first-of-type": {
                  transitionProperty: "width"
                }
              }}
            />
          </Tooltip>

          <Box>
            <Heading fontWeight={"semibold"} size={"lg"} alignItems="center">
              Study #{studyId}
            </Heading>
            <Metadata metadata={studyDetails} />
          </Box>
          <Divider />

          <Center
            alignSelf={"center"}
            data-testid={"events-timeline"}
            flexDirection="row"
            gap={3}
          >
            {allEvents.map((event, idx) => {
              return (
                <EventTimeline
                  isLast={idx === events.length - 1}
                  key={event.id}
                  title={event?.step_configuration?.name || "-"}
                  metadataConfigurations={
                    event.step_configuration?.metadata_configurations
                  }
                  kind={event.kind as Kind}
                  metadata={event.event_metadata}
                />
              );
            })}
          </Center>
        </VStack>
      </Container>

      <Box align-self={"center"} m={10}>
        <Text align={"center"}>
          Issue with this study? Contact system administrator at{" "}
          <Link
            href={`mailto:admin@botimage.com?subject=Study #${studyId} Report`}
            color={"#0072f5"}
          >
            admin@botimage.com
          </Link>
        </Text>
      </Box>
    </>
  );
}

export default withAuthenticated(StudyPage);
