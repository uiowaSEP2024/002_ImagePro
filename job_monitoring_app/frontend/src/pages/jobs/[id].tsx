/**
 * This file contains the JobPage component of the application.
 * The JobPage component is a React component that displays the details of a specific job.
 * It fetches the job data and the events associated with the job from the server, and displays them in a user-friendly format.
 * The job details include the job's name, date, time, customer ID, and provider.
 * The events are displayed in a timeline format, with each event represented by a timeline item.
 * The component also provides a feature for the user to report an issue with the job by sending an email to the system administrator.
 */

// Import necessary libraries, components, hooks, and types.
import { Metadata } from "@/components/Metadata";
import { EventTimeline } from "@/components/EventTimeline";
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchEvents, fetchJobById } from "@/data";
import { Job, JobEvent } from "@/data/types";
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

// Define the type for the JobEventWithNumber interface.
type JobEventWithNumber = JobEvent & { event_number: number };

/**
 * The JobPage component is a React component that displays the details of a specific job.
 * It fetches the job data and the events associated with the job from the server, and displays them in a user-friendly format.
 * The job details include the job's name, date, time, customer ID, and provider.
 * The events are displayed in a timeline format, with each event represented by a timeline item.
 * The component also provides a feature for the user to report an issue with the job by sending an email to the system administrator.
 */
function JobPage({ initialIsPageLoading = true }) {
  useEnsureAuthenticated();
  const router = useRouter();
  const { id: jobId } = router.query;
  const [events, setEvents] = useState<JobEventWithNumber[]>([]);
  const [job, setJob] = useState<Job | null>(null);
  const [isPageLoading, setIsPageLoading] = useState(initialIsPageLoading);

  const reversedEvents = useMemo(() => {
    return events.slice().reverse();
  }, [events]);

  const numSteps = useMemo(
    () => job?.job_configuration?.step_configurations.length,
    [job]
  );

  useEffect(() => {
    async function loadJob() {
      const data = await fetchJobById(jobId as unknown as number);
      if (data) setJob(data);
    }

    if (jobId) {
      loadJob();
    }
  }, [jobId]);

  // Derive the jobStatus based on the last event
  // If the last event is an error, the job is in an error state
  // If the job has num_steps, check if the number of step events matches the number of steps
  // Otherwise, check if the job has a complete event
  const jobStatus = useMemo(() => {
    const lastEvent = events.at(-1);

    if (lastEvent?.kind === "error") {
      return "error";
    }

    const hasCompleteEvent = events.some((event) => event.kind === "complete");
    return hasCompleteEvent ? "success" : "pending";
  }, [events]);

  useEffect(() => {
    const loadJobEvents = async () => {
      try {
        const data = await fetchEvents(jobId as unknown as number);
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
      await loadJobEvents();
      if (jobStatus === "success") {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [job, jobId, jobStatus]);

  // Derive the progress percentage based on either numSteps
  // if it is available, or do 0 -> 1 -> 50 -> 100 based on the presence of any events
  const progressAmount = useMemo(() => {
    if (numSteps) {
      const stepEvents = events.filter((event) => !!event.step_configuration);
      return ((stepEvents.length / numSteps) * 100).toFixed(0);
    }

    if (jobStatus === "success") {
      return 100;
    }

    if (events.length) {
      return 50;
    }

    return 1;
  }, [numSteps, jobStatus, events]);

  // Derive the color of the progress bar based on computed job status
  const progressColorScheme = useMemo((): ThemingProps["colorScheme"] => {
    if (jobStatus === "error") {
      return "red";
    }

    return "whatsapp";
  }, [jobStatus]);

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

  const jobDate = job?.created_at ? new Date(job?.created_at) : null;

  const jobDetails = {
    "Job Name": job?.job_configuration.name,
    Date: jobDate ? jobDate.toLocaleDateString() : "-",
    Time: jobDate ? jobDate.toLocaleTimeString() : "-",
    "Customer ID": job?.customer_id,
    Provider: job?.provider.first_name
  };

  return (
    <>
      <Container maxW="container.lg" py={"6"}>
        <VStack gap={"4"} w={"full"} align="left">
          <Link data-testid="backlink" href={"/jobs"}>
            <Button
              size={"md"}
              fontWeight={"semibold"}
              variant={"link"}
              _hover={{}}
              data-testid="backarrow"
              leftIcon={<ArrowBackIcon />}
            >
              Back to Jobs
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
              Job #{jobId}
            </Heading>
            <Metadata metadata={jobDetails} />
          </Box>
          <Divider />

          <Center
            alignSelf={"center"}
            data-testid={"events-timeline"}
            flexDirection="column"
            gap={2}
          >
            {reversedEvents.map((event, idx) => {
              return (
                <EventTimeline
                  isStart={idx === events.length - 1}
                  key={event.id}
                  title={event?.step_configuration?.name || "-"}
                  metadataConfigurations={
                    event.step_configuration?.metadata_configurations
                  }
                  kind={event.kind as any}
                  metadata={event.event_metadata}
                />
              );
            })}
          </Center>
        </VStack>
      </Container>

      <Box align-self={"center"} m={10}>
        <Text align={"center"}>
          Issue with this job? Contact system administrator at{" "}
          <Link
            href={`mailto:admin@botimage.com?subject=Job #${jobId} Report`}
            color={"#0072f5"}
          >
            admin@botimage.com
          </Link>
        </Text>
      </Box>
    </>
  );
}

export default withAuthenticated(JobPage);
